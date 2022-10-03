import logging
import json
from typing import Optional
import requests

from lmrtfy import _lmrtfy_template_dir
from lmrtfy.login import load_token_data, get_cliconfig


def fetch_template(profile_id):

    config = get_cliconfig()

    try:
        token = load_token_data()['access_token']
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', "Authorization": f"Bearer {token}"}
        url = config['api_profiles_url'] + f'/input_template/{profile_id}'
        rr = requests.get(url, headers=headers)
        if rr.status_code == 200:
            return rr.json()
        else:
            logging.error('Could not fetch template from server.')
    except:
        logging.error('Fetch template request failed.')


def save_json_template(profile_id, template):

    try:
        with open(_lmrtfy_template_dir.joinpath(f'{profile_id}.json'), 'w') as f:
            json.dump(template, f)
    except Exception:
        logging.error(f"Could not save template for profile {profile_id} in {_lmrtfy_template_dir}.")


def load_json_template(profile_id) -> Optional[dict]:

    try:
        with open(_lmrtfy_template_dir.joinpath(f'{profile_id}.json'), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f'Could not load template for profile {profile_id} in {_lmrtfy_template_dir}.')
        logging.info(f'Trying to fetch template for {profile_id}.')
        template = fetch_template(profile_id)
        if template:
            save_json_template(profile_id, template)
            return template

        exit(-1)


from lmrtfy.runner.runner import Runner
from lmrtfy.runner.runner import JobStatus, RunnerStatus
from lmrtfy.runner.__main__ import main