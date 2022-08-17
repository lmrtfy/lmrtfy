# -*- coding: utf-8 -*-

import os
import pathlib
import logging


logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG)

# Don't import or use the underscored variables. These are subject to change.
_user_home = pathlib.Path.home()

# TODO: respect system standard directories, for linux this is:
#  https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
#  issue #2
_lmrtfy_dir = _user_home.joinpath('.lmrtfy')
_lmrtfy_profiles_dir = _lmrtfy_dir.joinpath('profiles')
_lmrtfy_config_dir = _lmrtfy_dir.joinpath('config')

if not _lmrtfy_dir.is_dir():
    os.mkdir(_lmrtfy_dir)

if not _lmrtfy_profiles_dir.is_dir():
    os.mkdir(_lmrtfy_profiles_dir)

if not _lmrtfy_config_dir.is_dir():
    os.mkdir(_lmrtfy_config_dir)

from lmrtfy.annotation import resource
from lmrtfy.annotation import variable
from lmrtfy.annotation import result
from lmrtfy import runner
