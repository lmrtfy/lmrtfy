#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
os.environ['LMRTFY_DEPLOY_LOCAL'] = "1"

import fire
import pathlib
import lmrtfy.runner
from lmrtfy.login import LoginHandler


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

        if local:
            lmrtfy.runner.main(pathlib.Path(script_path).resolve())
        else:
            print("This feature is not yet implemented. Please run 'lmrtfy deploy --local' for now.")


def main():
    fire.Fire(LMRTFY)
