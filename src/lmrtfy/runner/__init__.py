import logging
import json
from typing import Optional
from lmrtfy import _lmrtfy_template_dir


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


from lmrtfy.runner.runner import Runner
from lmrtfy.runner.__main__ import main
