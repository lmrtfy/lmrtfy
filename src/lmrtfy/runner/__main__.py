#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import requests
import yaml
import json
import logging

from lmrtfy.runner import Runner, save_json_template
from lmrtfy import _lmrtfy_profiles_dir
from lmrtfy.login import load_token_data, LoginHandler, get_cliconfig


def main(script_path: Path):

    config = get_cliconfig()
    _script_path = str(Path(script_path).resolve())

    _script_identifier = _script_path.replace('/', '_').replace('\\', '_').replace('.', '_')
    _lmrtfy_profile_filename = _lmrtfy_profiles_dir.joinpath(f'{_script_identifier}.yml')

    url = config['api_catalog_url']
    try:
        with open(_lmrtfy_profile_filename, "r") as p:
            data = {"profile": yaml.safe_load(p)}

    except FileNotFoundError:
        logging.error(f"No profile for {script_path} found. Please run first without the lmrtfy cli.")
        exit(-1)

    # TODO: This has been caught elsewhere and can be removed/rewritten.
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
            logging.error('No auth token found. Authentication failed.')
            exit(-1)

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain', "Authorization": f"Bearer {token}"}
    r = requests.post(url, data=json.dumps(data), headers=headers)

    if r.status_code == 202 or r.status_code == 200:
        profile_id = r.json()['profile_id']
        logging.info(f"Profile_id to be used for requests: {profile_id}")

        try:
            url = config['api_profiles_url'] + f'/input_template/{profile_id}'
            rr = requests.get(url, headers=headers)
            save_json_template(profile_id, rr.json())
        except:
            logging.error('Could not get input template.')
    else:
        logging.error('Deployment failed.')
        exit(-1)

    r = Runner(broker_url=config['broker_url'], port=int(config['broker_port']), profile_path=_lmrtfy_profile_filename)

    r.start_listening()
