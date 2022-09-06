#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import fire
import pathlib
import lmrtfy.runner
import requests
import lmrtfy
from lmrtfy.login import LoginHandler, load_token_data, get_cliconfig
from lmrtfy.runner import load_json_template
import json
import logging
import coloredlogs
from lmrtfy.fetch_results import fetch_results
from pathlib import Path
from packaging import version

_log_level = logging.INFO
if 'LMRTFY_DEBUG' in os.environ:
    _log_level = logging.DEBUG

coloredlogs.install(fmt='%(asctime)s [%(process)d] %(levelname)s %(message)s', level=_log_level)


def check_version():
    try:
        r = requests.get("https://pypi.org/pypi/lmrtfy/json")
        recent_version = version.parse(str(list(r.json()['releases'].keys())[-1]))
        installed_version = version.parse(str(lmrtfy.__version__))

        if installed_version < recent_version:
            logging.warning(f"A new version ({recent_version}) is available. Please run: 'pip install --upgrade lmrtfy'")
    except:
        logging.warning("Version check failed")


class LMRTFY(object):
    """ Let me run that for you.
        Easily deploy your scripts to accept input via a web API.
    """

    def __init__(self):
        check_version()
        logging.info('Start LMRTFY command line interface.')

    def login(self):
        """
        Login to the LMRTFY cloud service.
        By using this tool you accept the terms and conditions.
        """
        logging.info('Authenticating for LMRTFY.')
        h = LoginHandler()
        if h.login():
            h.get_token()

    def deploy(self, script_path: str, local: bool = False):
        """
        Deploy your script to accept inputs via web-api.

        :param script_path: script to be deployed (full path)
        :param local: deployment on this host only (script is executed locally)
        """

        self.login()

        logging.info(f'Starting deployment of {script_path}')
        if local:
            logging.warning('Deploying locally.')
            lmrtfy.runner.main(pathlib.Path(script_path).resolve())
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
            exit(-1)

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
                    logging.warning(f"Reason: \"{r.json()}\"")
        except FileNotFoundError:
            logging.error(f"Opening input file {input_file} failed.")

    def fetch(self, job_id: str, results_dir: str = None):
        """
        Fetch results of a job for a given job id.

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
                    r.write(content)
            except IOError:
                logging.error(f"Could not write results {name}")


def main():
    fire.Fire(LMRTFY)
