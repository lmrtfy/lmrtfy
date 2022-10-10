#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import fire
import pathlib
import requests
from lmrtfy.runner import load_json_template
import json
import logging
from pathlib import Path
from packaging import version

import coloredlogs

import lmrtfy
import lmrtfy.runner
from lmrtfy.login import LoginHandler, load_token_data, get_cliconfig
from lmrtfy.runner import load_json_template
from lmrtfy.fetch_results import fetch_results


_log_level = logging.INFO
if 'LMRTFY_DEBUG' in os.environ:
    _log_level = logging.DEBUG

coloredlogs.install(fmt='%(asctime)s [%(process)d] %(levelname)s %(message)s', level=_log_level)


def check_version():
    installed_version = version.parse(str(lmrtfy.__version__))
    logging.info(f"Running lmrtfy version {installed_version}.")

    try:
        r = requests.get("https://pypi.org/pypi/lmrtfy/json")
        recent_version = version.parse(str(list(r.json()['releases'].keys())[-1]))

        if installed_version < recent_version:
            logging.warning(f"A new version ({recent_version}) is available. Please run: 'pip install --upgrade lmrtfy'")
    except:
        logging.warning("Version check failed")


class LMRTFY(object):
    """ Let me run that for you.
        Easily deploy your scripts to accept input via a web API.
    """

    def __init__(self):
        logging.info('LMRTFY command line interface')
        check_version()
        self._login_handler = LoginHandler()

    def logout(self):
        """
        Logout from the LMRTFY cloud service
        """
        self._login_handler.logout()

    def login(self):
        """
        Login to the LMRTFY cloud service.
        By using this tool you accept the terms and conditions.
        """

        if "LMRTFY_LOCAL" in os.environ:
            logging.warning("Using the local API.")
        elif "LMRTFY_DEV" in os.environ:
            logging.warning("Using the development API.")

        logging.info('Authenticating for LMRTFY.')
        if self._login_handler.login():
            self._login_handler.get_token()

    def deploy(self, script_path: str, local: bool = False, run_as_daemon: bool = False, namespace: str=""):
        """
        Deploy your script to accept inputs via web-api.

        :param namespace:
        :param script_path: script to be deployed (full path)
        :param local: deployment on this host only (script is executed locally)
        :param run_as_daemon: run local deployment as daemon (in background)
        """

        self.login()

        logging.info(f'Starting deployment of {script_path}')
        if local:

            if run_as_daemon:
                from daemon import DaemonContext as Context
            else:
                from lmrtfy.helper import Context

            logging.warning('Deploying locally.')
            with Context(working_directory='./') as c:
                lmrtfy.runner.main(pathlib.Path(script_path).resolve(), namespace)
        else:
            logging.warning('Deploying to cloud.')
            logging.error("This feature is not yet implemented. Please run 'lmrtfy deploy <script> --local' for now.")

    def submit(self, profile_id: str, input_file: str = None):
        """
        Submit a job to a deployed script via the web.

        :param profile_id: Profile id of the script that you want to run.
        :param input_file: JSON file that serves as the input of the job. Run once without specified
        file to get template.
        """
        self.login()

        if not input_file:
            logging.error('No input file given. Use this template to create one.')
            template = load_json_template(profile_id)
            msg = json.dumps(template, indent=4).split('\n')
            for m in msg:
                logging.warning(m)
            sys.exit(-1)

        try:
            with open(input_file, 'r') as f:
                config = get_cliconfig()
                token = load_token_data()['access_token']
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain', "Authorization": f"Bearer {token}"}
                j = json.load(f)
                d = json.dumps(j)
                logging.info("Submitting job with parameters: ")
                msg = json.dumps(j, indent=4).split('\n')
                for m in msg:
                    logging.warning(m)
                r = requests.post(config['api_submit_url'] + f'/{profile_id}', data=d, headers=headers)
                if r.status_code == 200:
                    logging.info("Job submission successful.")
                    logging.info(f"Job-id: {r.json()['job_id']}")
                else:
                    logging.error("Job submission unsuccessful.")
                    logging.warning(f"Reason: \"{r.text}\"")
        except FileNotFoundError:
            logging.error(f"Opening input file {input_file} failed.")

    def fetch(self, job_id: str, results_dir: str = None):
        """
        Fetch results of a job for a given job id.

        :param results_dir:  Directory where to put the results. Default is './'
        :param job_id: Job id of the job that you want to fetch results for.
        """
        self.login()

        logging.info(f'Fetching results for job-id {job_id}')

        results = fetch_results(job_id)

        if results_dir:
            p = Path(results_dir).joinpath(job_id)
        else:
            p = Path('./').joinpath(job_id)

        p.mkdir(exist_ok=True)

        logging.info(f'Writing results in {p.resolve()}')
        for name, content in results.items():
            try:
                logging.info(f"Writing results {name}.")
                with open(p.joinpath(name), "w") as r:
                    json.dump({name: content}, r)
            except IOError:
                logging.error(f"Could not write results {name}")


def main():
    fire.Fire(LMRTFY)
