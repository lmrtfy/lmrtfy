#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from makefun import create_function
from inspect import Signature, Parameter
import requests
from lmrtfy.login import LoginHandler, load_token_data, get_cliconfig
from lmrtfy.runner import fetch_template
from lmrtfy import _lmrtfy_job_dir
import numpy.typing as npt
from typing import List, Optional, Type
import json
from lmrtfy.helper import NumpyEncoder
import enum


typemap = dict()
typemap['int'] = int
typemap['float'] = float
typemap['complex'] = complex
typemap['string'] = str
typemap['float_array'] = npt.NDArray[float]
typemap['int_array'] = npt.NDArray[int]
typemap['string_array'] = List[str]
typemap['json'] = dict
typemap['bool'] = bool


class JobStatus(str, enum.Enum):
    IDLE = "IDLE"
    WAITING = "WAITING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    JOB_RECEIVED = "JOB_RECEIVED"
    RUNNING = "RUNNING"
    RESULTS_READY = "RESULTS_READY"
    INCOMPLETE_RESULTS = "INCOMPLETE_RESULTS"
    ABORTED = "ABORTED"
    UNKNOWN = "UNKNOWN"


class Job(object):

    def __init__(self, job_id):
        self.id = job_id
        logging.info(f"Job {self.id} created. Status is {self.status}.")

    @property
    def status(self):
        try:
            token = load_token_data()['access_token']
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain', "Authorization": f"Bearer {token}"}
            r = requests.get(get_cliconfig()['api_submit_url'][:-1] + f'jobs/{self.id}', headers=headers)
            status = JobStatus(r.json())
        except:
            status = JobStatus.UNKNOWN

        try:
            with open(_lmrtfy_job_dir.joinpath(f"{self.id}.job"), "w") as f:
                json.dump({"id": self.id, "status": status}, f)
        except:
            logging.error(f"Could not write local job-file for job {self.id}.")

        return status

    @property
    def results(self):
        # TODO: use fetch_results from the corresponding file
        try:
            config = get_cliconfig()
            token = load_token_data()['access_token']
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain', "Authorization": f"Bearer {token}"}
            r = requests.get(config['api_results_url'] + f"/{self.id}", headers=headers)
            # TODO: Store results locally and delete job_file.
            if r.status_code == 200:
                return r.json() #json.loads(r.json())
            else:
                logging.error(f"Could not fetch results from server: {r.status_code}")
        except ConnectionError as e:
            logging.error("Could not access results server.")
            logging.error(e.strerror)

    @property
    def ready(self):
        if self.status == JobStatus.RESULTS_READY:
            return True
        return False


def unique_name(o, name):
    new_name = name

    if hasattr(o, new_name):
        logging.warning(f"Function {new_name} already exists in catalog!")
        suffix = 1

        while True:
            new_name = name + str(suffix)
            if not hasattr(o, new_name):
                break
            suffix += 1

    return new_name


def signature_from_profile(profile):
    parameters = list()
    for v in profile['variables']:
        parameters.append(
            Parameter(v, kind=Parameter.POSITIONAL_OR_KEYWORD, annotation=typemap[profile['variables'][v]['dtype']]))

    results = list()
    for v in profile['results']:
        results.append(typemap[profile['results'][v]['dtype']])
    results = tuple(results)

    sig = Signature(parameters, return_annotation=Optional[Type[Job]])

    return sig, results


def fetch_profile(profile_id):

    try:
        config = get_cliconfig()
        token = load_token_data()['access_token']
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', "Authorization": f"Bearer {token}"}
        url = config['api_profiles_url'] + f'/{profile_id}'
        rr = requests.get(url, headers=headers)
        if rr.status_code == 200:
            return rr.json()
        else:
            logging.error('Could not fetch template from server.')
    except:
        logging.error('Fetch template request failed.')


class Catalog(object):
    """
    The Catalog object provides an interface to deployed functions that you can run from your code.

    Cloud functions are pulled into the catalog by the constructor, which happens during `from lmrtfy
    import catalog`.

    If you want to retrieve newly deployed function, call `catalog.update()`.

    To run a deployed function from the catalog call `catalog.<deployed_function>(*args, **kwargs)`.

    Each function that has been pulled into the catalog is available via the `help()` command.
    """
    def __init__(self):
        h = LoginHandler()
        if h.login():
            h.get_token()

        self.config = get_cliconfig()

        self.token = load_token_data()['access_token']
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain',
                        "Authorization": f"Bearer {self.token}"}

        self.profiles = None
        self.update()

    def update(self):
        """
        Call `update` to update the catalog with newly deployed functions.
        """
        try:
            r = requests.get(self.config['api_catalog_url'], headers=self.headers)
            if r.status_code == 200:
                self.profiles = r.json()
                logging.info("Updated function catalog.")
                for profile in self.profiles['profiles']:
                    pid = profile.split('/')[-1]
                    t = fetch_profile(pid)
                    func_name = unique_name(self, t['filename'].replace('\\', '/').split('/')[-1].split('.')[0].strip())
                    logging.info(f"Added function {func_name}.")
                    self.__add_function(func_name, *signature_from_profile(t), pid=pid)
        except:  # TODO: Except clause too broad!
            logging.error("Could not update function catalog.")

    def __add_function(self, name, sig, res_ann, pid):

        template = fetch_template(pid)

        def f(**kwargs) -> Job:
            for p in kwargs:
                template['argument_values'][p] = kwargs[p]
            r = requests.post(self.config['api_submit_url'] + f'/{pid}', data=json.dumps(template, cls=NumpyEncoder),
                              headers=self.headers)
            if r.status_code == 200:
                return Job(r.json()['job_id'])
            if r.status_code == 400:
                logging.error(f'Input Error: {r.json()}')

        setattr(self, name, create_function(sig, f, func_name=name))


catalog = Catalog()
