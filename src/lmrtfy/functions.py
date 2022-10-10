#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from makefun import create_function
from inspect import Signature, Parameter
import requests

import numpy.typing as npt
from typing import List, Optional, Type
import json
import jwt

import coloredlogs

from lmrtfy.login import LoginHandler, load_token_data, get_cliconfig
from lmrtfy.runner import fetch_template
from lmrtfy.runner import JobStatus
from lmrtfy import _lmrtfy_job_dir
from lmrtfy.helper import NumpyEncoder
from lmrtfy.fetch_results import fetch_results


_log_level = logging.INFO
if 'LMRTFY_DEBUG' in os.environ:
    _log_level = logging.DEBUG

coloredlogs.install(fmt='%(asctime)s [%(process)d] %(levelname)s %(message)s', level=_log_level)


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


class Job(object):

    def __init__(self, job_id):
        self.id = job_id
        logging.info(f"Job {self.id} created. Status is {self.status}.")


    @property
    def status(self):
        """
        Queries the job status.

        If it returns `JobStatus.UNKNOWN` the job is likely in failed state.
        """
        try:
            token = load_token_data()['access_token']
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain', "Authorization": f"Bearer {token}"}
            r = requests.get(get_cliconfig()['api_job_url'] + f'/{self.id}', headers=headers)
            status = JobStatus(r.json())
        except Exception as e:
            logging.error(e)
            status = JobStatus.UNKNOWN

        try:
            with open(_lmrtfy_job_dir.joinpath(f"{self.id}.job"), "w") as f:
                json.dump({"id": self.id, "status": status}, f)
        except:
            logging.error(f"Could not write local job-file for job {self.id}.")

        return status

    @property
    def results(self) -> Optional[dict]:
        """
        Returns the results if they are ready and `None` otherwise.
        Results are returned as a dictionary:
        ```json
        {
            "<results_name>": result_value
        }
        ```
        """
        return fetch_results(self.id)

    @property
    def ready(self):
        """
        Returns `True` if the job has finished successfully and the results are ready to be fetched.
        """
        if self.status == JobStatus.RESULTS_READY:
            return True
        return False


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


class Namespace(object):

    def __init__(self, name):
        self.__name__ = name


class Catalog(object):
    """
    The Catalog object provides an interface to deployed functions that you can run from your code.

    Cloud functions are pulled into the catalog by the constructor, which happens during `from lmrtfy
    import catalog`.

    If you want to retrieve newly deployed function, call `catalog.update()`.

    To run a deployed function from the catalog call `catalog.<namespace>.<deployed_function>(*args, **kwargs)`.

    Each function that has been pulled into the catalog is available via the `help()` command.
    """
    def __init__(self):
        h = LoginHandler()
        if h.login():
            h.get_token()

        self.config = get_cliconfig()
        logging.info(self.config)
        self.token = load_token_data()['access_token']
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain',
                        "Authorization": f"Bearer {self.token}"}

        self.profiles = None
        self.update()

    def __add_function(self, namespace, name, sig, res_ann, pid, template):

        template = fetch_template(pid)

        def f(**kwargs) -> Job:
            f.pid = pid
            for p in kwargs:
                template['argument_values'][p] = kwargs[p]

            r = requests.post(self.config['api_submit_url'] + f'/{pid}',
                              data=json.dumps(template, cls=NumpyEncoder),
                              headers=self.headers)

            if r.status_code == 200:
                return Job(r.json()['job_id'])
            if r.status_code == 400:
                logging.error(f'Input Error: {r.json()}')
            elif r.status_code == 404:
                logging.error(f"{r.json()}")

        setattr(namespace, name, create_function(sig, f, func_name=name, qualname=f"{namespace.__name__}-{pid}"))

    def update(self):
        """
        Call `update` to update the catalog with newly deployed functions.
        """

        r = requests.get(self.config['api_namespaces_url'], headers=self.headers)
        logging.info(r.json())
        namespaces = r.json()['namespaces']

        for n in namespaces:
            try:
                delattr(self, n.split('/')[0])
            except:
                pass

        for n in namespaces:
            names = n.split('/')
            o = self
            nsn = ""
            for name in names:
                nsn += f"{name}/"
                if not hasattr(o, name):
                    setattr(o, name, Namespace(nsn[:-1]))
                o = getattr(o, name)

            try:
                r = requests.get(f"{self.config['api_namespaces_url']}/{n.replace('/','-')}", headers=self.headers)
                functions = r.json()['functions']

                for func in functions:
                    func_name = functions[func]['name']
                    if not hasattr(o, func_name):
                        self.__add_function(o, func_name, *signature_from_profile(functions[func]), pid=func, template=functions[func])

            except:  # TODO: Except clause too broad!
                logging.error(f"Could not namespace {n} function catalog.")

    def create_namespace(self, namespace: Namespace, name: str) -> bool:
        """
        Create a unique namespace that collects functions and can be shared.

        Example:
        ```python
        catalog.create_namespace(catalog.<namespace>, "new_namespace")
        ```

        :param namespace: parent namespace
        :param name: Name of the new namespace.
        :return: Returns the `True` on success and `False` in case of an error.
        """
        try:
            new_name = f"{namespace.__name__}/{name}".replace('/', '-')
            r = requests.post(f"{self.config['api_namespaces_url']}",
                              data=json.dumps({"namespace": new_name}), headers=self.headers)
            if r.status_code == 201:
                self.update()
                return True
        except:
            pass

        logging.error(f"Could not create namespace {name}.")

        return False

    def add_function_to_namespace(self, namespace: Namespace, function):
        """
        Add a function to an existing namespace.

        Example:
        ```python
        catalog.add_function_to_namespace(catalog.<namespace>, catalog.<namespace>.<function>
        ```
        """
        # PUT
        r = requests.put(f"{self.config['api_namespaces_url']}/{namespace.__name__.replace('/', '-')}",
                         data=json.dumps({'function': function.__qualname__.split('-')[-1]}), headers=self.headers)
        if r.status_code == 202:
            self.update()
            return True

        return False

    def delete_namespace(self, namespace: Namespace) -> bool:
        """
        Deletes the entire namespace. Deletion will fail if there are still functions in the
        namespace.
        """
        # DELETE
        r = requests.delete(f"{self.config['api_namespaces_url']}/{namespace.__name__.replace('/', '-')}",
                            headers=self.headers)
        if r.status_code == 202:
            self.update()
            return True

        return False

    def remove_function_from_namespace(self, function) -> bool:
        """
        Delete `function` from its namespace.
        """
        # PATCH
        namespace = function.__qualname__.split('-')[0]
        r = requests.patch(f"{self.config['api_namespaces_url']}/{namespace.replace('/', '-')}",
                         data=json.dumps({'function': function.__qualname__.split('-')[-1]}), headers=self.headers)
        if r.status_code == 202:
            self.update()
            return True

        return False

    def share_namespace(self, namespace: Namespace, recipient_email: str) -> Optional[str]:
        """
        Share a namespace with someone else by email. The invite email will be sent to `recipient_email`.
        This does not have to be the email address associated with the account of the person you
        want to share the namespace with.

        Invites only work once.
        """
        id_token = load_token_data()['id_token']
        sender_email = jwt.decode(id_token, options={"verify_signature": False})["email"]
        r = requests.post(f"{self.config['api_invites_url']}",
                          data=json.dumps({"namespace": namespace.__name__,
                                           "recipient_email": recipient_email,
                                           "sender_email": sender_email}), headers=self.headers)

        if r.status_code == 202:
            return r.json()["invite_id"]

    def accept_invite(self, invite_id) -> bool:
        r = requests.get(f"{self.config['api_invites_url']}/{invite_id}", headers=self.headers)
        if r.status_code == 202:
            self.update()
            return True

        return False


catalog = Catalog()
