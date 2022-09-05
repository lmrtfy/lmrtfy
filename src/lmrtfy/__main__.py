#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fire
import pathlib
import lmrtfy.runner
from lmrtfy.login import LoginHandler
import logging
import coloredlogs
coloredlogs.install(fmt='%(asctime)s [%(process)d] %(levelname)s %(message)s')


class LMRTFY(object):
    """ Let me run that for you.
        Easily deploy your scripts to accept input via web-api.
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


def main():
    fire.Fire(LMRTFY)
