#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import toml
from pathlib import Path
import requests
import yaml
import json
import logging

from lmrtfy.runner import Runner
from lmrtfy import _lmrtfy_config_dir, _lmrtfy_profiles_dir
from lmrtfy.login import load_token_data, LoginHandler, get_cliconfig


def main(script_path: Path):

    config = get_cliconfig()
    _script_path = str(Path(script_path).resolve())

    _script_identifier = _script_path.replace('/', '_').replace('\\', '_').replace('.', '_')
    _lmrtfy_profile_filename = _lmrtfy_profiles_dir.joinpath(f'{_script_identifier}.yml')

    url = config['api_catalog_url']
    with open(_lmrtfy_profile_filename, "r") as p:
        data = {"profile": yaml.safe_load(p)}

    token = ''
    try:
        token = load_token_data()['access_token']
    except Exception:
        h = LoginHandler()
        if h.login():
            h.get_token()
        try:
            token = load_token_data()['access_token']
        except Exception:
            # TODO: Nice message when no token is available and login fails.
            exit(-1)

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain', "Authorization": f"Bearer {token}"}
    r = requests.post(url, data=json.dumps(data), headers=headers)

    if r.status_code == 202:
        logging.info(f"Profile_id to be used for requests: {r.json()['profile_id']}")

    r = Runner(broker_url=config['broker_url'], port=int(config['broker_port']), profile_path=_lmrtfy_profile_filename)

    r.start_listening()
