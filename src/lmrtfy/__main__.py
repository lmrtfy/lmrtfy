#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fire
import pathlib
import lmrtfy.runner
from lmrtfy.login import LoginHandler
import coloredlogs
coloredlogs.install(fmt='%(asctime)s [%(process)d] %(levelname)s %(message)s')

import logging


class LMRTFY(object):
    """ Maybe this gets printed """

    def login(self):
        """
        This is shit
        :return:
        """
        h = LoginHandler()
        if h.login():
            h.get_token()

    def deploy(self, script_path: str, local: bool = False):

        self.login()

        if local:
            lmrtfy.runner.main(pathlib.Path(script_path).resolve())
        else:
            print("This feature is not yet implemented. Please run 'lmrtfy deploy --local' for now.")


def main():
    fire.Fire(LMRTFY)
