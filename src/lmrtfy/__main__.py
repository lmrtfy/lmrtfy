# -*- coding: utf-8 -*-
import fire

def _deploy(local: bool = False):
    if local:
        print("haha")
    else:
        print("sad")


def _analyze(script: str):
    print("analyze")

def _run():
    print("jiiihaaa")

def main():
    fire.Fire({
        "": _run,
        "analyze": _analyze,
        "deploy": _deploy
    })
