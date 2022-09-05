#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fire
import pathlib
import lmrtfy.runner
import requests
from lmrtfy.login import LoginHandler, load_token_data, get_cliconfig
from lmrtfy.runner import load_json_template
import json
import logging
import coloredlogs
coloredlogs.install(fmt='%(asctime)s [%(process)d] %(levelname)s %(message)s', level=logging.DEBUG)


class LMRTFY(object):
    """ Let me run that for you.
        Easily deploy your scripts to accept input via a web API.
    """

    def __init__(self):
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
            template = load_json_template(profile_id)
            logging.error('No input file given. Use this template to create one.')
            logging.warning(template)
            exit(-1)

        #try:
        with open(input_file, 'r') as f:
            config = get_cliconfig()
            token = load_token_data()['access_token']
            #print(token)
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain', "Authorization": f"Bearer {token}"}
            d = json.dumps(json.load(f))
            #print(d)
            r = requests.post(config['api_submit_url'] + f'/{profile_id}', data=d, headers=headers)
            #print(r.content)
            if r.status_code == 200:
                logging.info("Job submission successful.")
                logging.info(f"Job-id: {r.json()['job_id']}")
            else:
                logging.info("Job submission unsuccessful.")
                logging.info(f"Reason: \"{r.json()}\"")
        #except:
        #    logging.error("Job submission failed.")

    def fetch(self, job_id: str):
        pass


def main():
    fire.Fire(LMRTFY)
