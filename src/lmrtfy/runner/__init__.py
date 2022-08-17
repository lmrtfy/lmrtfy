#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import toml
from pathlib import Path
import requests
import yaml
import json
import logging

from .runner import Runner
from lmrtfy import _lmrtfy_config_dir, _lmrtfy_profiles_dir


def main(script_path: Path):
    with open(_lmrtfy_config_dir.joinpath("config.toml"), "r") as c:
        config = toml.load(c)

    broker_url = config["broker"]["url"]
    broker_port = config["broker"]["port"]
    broker_user = config["broker"]["username"]
    broker_pw = config["broker"]["password"]

    _script_path = str(Path(script_path).resolve())

    _script_identifier = _script_path.replace('/', '_').replace('\\', '_').replace('.', '_')
    _lmrtfy_profile_filename = _lmrtfy_profiles_dir.joinpath(f'{_script_identifier}.yml')

    url = 'http://api.simulai.de/catalog'
    with open(_lmrtfy_profile_filename, "r") as p:
        data = {"profile": yaml.safe_load(p)}

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)

    if r.status_code == 202:
        logging.info(f"Profile_id to be used for requests: {r.json()['profile_id']}")

    r = Runner(
        broker_url=broker_url,
        port=broker_port,
        username=broker_user,
        password=broker_pw,
        profile_path=_lmrtfy_profile_filename
    )

    r.start_listening()
