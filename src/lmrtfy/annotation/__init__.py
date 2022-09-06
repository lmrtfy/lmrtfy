# -*- coding: utf-8 -*-

import sys
import os
import pathlib
import json
import logging
from typing import Union
from lmrtfy.helper import NumpyEncoder
import coloredlogs

import filehash
import yaml
import numpy as np

from .. import _lmrtfy_profiles_dir


# TODO: talk about file naming convention!
# TODO: Hacky hack. This should be changed.
_script_path = None
if sys.argv:
    if len(sys.argv) > 0:
        if len(sys.argv[0]) > 0:
            _script_path = pathlib.Path(sys.argv[0]).resolve()
            if len(sys.argv[0]) >= len('lmrtfy'):
                if sys.argv[0][-6:] == 'lmrtfy':
                    _script_path = None
                else:
                    coloredlogs.install(fmt='%(levelname)s %(message)s')


_run_deployed = False
_tmp_dir = None


if 'LMRTFY_DEPLOY_LOCAL' in os.environ and 'LMRTFY_TMP_DIR' in os.environ:
    logging.info("Running deployed.")
    _run_deployed = bool(int(os.environ['LMRTFY_DEPLOY_LOCAL']))
    _tmp_dir = pathlib.Path(os.environ['LMRTFY_TMP_DIR'])
    logging.info(f"Running: data dir is '{_tmp_dir}'")


if _script_path:
    _sha1hasher = filehash.FileHash('sha1')
    _hash = _sha1hasher.hash_file(_script_path)

    profile = {}
    profile['language'] = 'python'
    profile['filename'] = str(_script_path)
    profile['filehash'] = _hash
    profile['variables'] = {}
    profile['results'] = {}


if not _run_deployed:
    if _script_path:
        _script_identifier = str(_script_path).replace('/', '_').replace('\\', '_').replace('.', '_')
        _lmrtfy_profile_filename = _lmrtfy_profiles_dir.joinpath(f'{_script_identifier}.yml')
        _lmrtfy_profile_filename.touch()

if not _run_deployed and _script_path:
    with open(_lmrtfy_profile_filename,'w') as f:
        yaml.dump(profile, f)
        logging.info(f"Wrote profile to {str(_lmrtfy_profile_filename)}.")


_types = ['json', 'string', 'string_array', 'int', 'int_array', 'float', 'float_array', 'complex',
          'complex_array', 'bool', 'bool_array']
_type_map = {int:'int', bool: 'bool', str: 'string', float: 'float'}
_inverse_type_map = {type(1): int, type(True): bool, type("abc"): str, type(1.1): float,
                     type({}): dict, type(np.zeros(3)): np.asarray, type([]): list}


# a type definition in order to have type hint for variable and result function
supported_object_type = Union[int, float, complex, bool, np.ndarray, list, dict]


def _add_to_api_definition(name: str, kind: str, dtype: str, min = None, max = None,
                           unit: str = None):
    if not _run_deployed and _script_path:
        with open(_lmrtfy_profile_filename, 'r') as p:
            profile = yaml.full_load(p)

        if name in profile[f'{kind}s']:
            logging.error(f"{kind.capitalize()} with name '{name}' already exists! "
                          f"Change the 'name' property in the '{kind}' call.")
            logging.error("Analyzer: Profiling failed. Exiting. Fix the errors above ^^^^^.")
            sys.exit(1)

        logging.info(f"Analyzer: Adding {kind} with name '{name}'")
        profile[f'{kind}s'][name] = {}

        if dtype:
            logging.info(f"Analyzer: Adding datatype '{dtype}' for {kind} with name '{name}'")
            profile[f'{kind}s'][name]['dtype'] = dtype
        if min:
            logging.info(f"Analyzer: Adding minimum value '{min}' for {kind} with name '{name}'")
            profile[f'{kind}s'][name]['min'] = min
        if max:
            logging.info(f"Analyzer: Adding maximum value '{max}' for {kind} with name '{name}'")
            profile[f'{kind}s'][name]['max'] = max
        if unit:
            logging.info(f"Analyzer: Adding unit '{unit}' for {kind} with name '{name}'")
            profile[f'{kind}s'][name]['unit'] = unit

        with open(_lmrtfy_profile_filename, 'w') as f:
            yaml.dump(profile, f)


def _get_type(a: supported_object_type) -> str:
    """
    Returns the type of `a` as a string.

    Supported types: int, float, complex
    :param a: Object to get type of
    :return: type of the object
    :rytpe: string
    """
    if type(a) in [int, str, bool]:
        return _type_map[type(a)]
    try:
        import numpy as np
        for t in ['int', 'float', 'complex']:
            if t in str(type(a)):
                return t
        if type(a) in [np.ndarray, ]:
            for t in ['int', 'float', 'complex', 'bool']:
                if t in str(a.dtype):
                    return f"{t}_array"
    except ImportError:
        logging.warning("Analyzer: numpy is not available, so I'm assuming you don't need it "
                        "either.")

    if type(a) in [list, tuple, set]:
        if len(a) > 0:
            if len(set([type(el) for el in a])) > 1:
                return "json"
            for t in ['int', 'float', 'complex', 'bool']:
                if t in str(type(a[0])):
                    return f"{str(t)}_array"
            if 'str' in str(type(a[0])):
                return "string_array"
        return "json"

    if type(a) == dict:
        return "json"


def resource(a):
    """ This is a filepath, address or URL.
    :param a:
    :return:
    """
    return a


def variable(a: supported_object_type, name: str, min = None, max = None,
             unit: str = None) -> supported_object_type:
    """
    :param a:
    :param name:
    :param min:
    :param max:
    :param unit:
    :return:

    """
    _add_to_api_definition(name, kind='variable', dtype=_get_type(a), min=min, max=max, unit=unit)

    if _run_deployed and _tmp_dir and _script_path:
        # TODO: warn and except if something fails.
        with open(str(_tmp_dir.joinpath(f'lmrtfy_variable_{name}.json')), 'r') as f:
            tmp = json.load(f)
            # TODO: Make it work for numpy dtypes.
            dtype = _inverse_type_map[type(a)]
            a = dtype(tmp[name])
            logging.info(f"Running: Loaded variable '{name}' of type '{dtype}' and value '{a}'.")

    return a


# TODO: argument ordering is not the same as in variable Issue#7
def result(a: supported_object_type, name: str, min = None, max = None,
           unit: str = None) -> supported_object_type:
    """
    :param a:
    :param name:
    :param min:
    :param max:
    :param unit:
    :return:
    """
    _add_to_api_definition(name, kind='result', dtype=_get_type(a), unit=None, min=min, max=max)

    if _run_deployed and _tmp_dir and _script_path:
        # TODO: warn and except if something fails.
        with (open(str(_tmp_dir.joinpath(f'lmrtfy_result_{name}.json')), 'w')) as f:
            json.dump({name: a}, f, cls=NumpyEncoder)
            logging.info(f"Running: Saved result '{name}' with value '{a}'.")

    return a
