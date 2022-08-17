#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib

import fire
import lmrtfy.runner


def _deploy(local: bool = False, script_path: str = None):
    if local:
        print(script_path)
        lmrtfy.runner.main(pathlib.Path(script_path).resolve())
    else:
        print("This feature is not yet implemented. Please run 'lmrtfy deploy --local' for now.")




def main():
    fire.Fire({
        "deploy": _deploy
    })
