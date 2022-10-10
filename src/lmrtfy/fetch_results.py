#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from typing import Optional
import requests
from sys import exit

from lmrtfy.login import load_token_data, get_cliconfig



def fetch_results(job_id: str) -> Optional[dict]:
    try:
        config = get_cliconfig()
        token = load_token_data()['access_token']
        headers = {
            'Content-type': 'application/json',
            'Accept': 'text/plain',
            "Authorization": f"Bearer {token}"
        }
        # TODO: /user/{job_id} is a workaround as of now. not ideal.
        r = requests.get(config['api_results_url'] + f"/user/{job_id}", headers=headers)
        if r.status_code == 200:
            return r.json()
        else:
            logging.error(f"Could not fetch results from server: {r.status_code}")
            logging.error(f"Reason: {r.json()}")

    except ConnectionError as e:
        logging.error("Could not access results server.")
        logging.error(e.strerror)
        exit(-1)
