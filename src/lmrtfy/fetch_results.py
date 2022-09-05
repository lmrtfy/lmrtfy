#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import requests
from sys import exit

from lmrtfy.login import load_token_data, get_cliconfig


def fetch_results(job_id: str):

    try:
        config = get_cliconfig()
        token = load_token_data()['access_token']
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', "Authorization": f"Bearer {token}"}
        r = requests.get(config['api_results_url'] + f"/{job_id}", headers=headers)
        if r.status_code == 200:
            return r.json()
        else:
            logging.error(f"Could not fetch results from server: {r.status_code}")
            exit(-1)
    except:
        logging.error("Could not access results server.")
        exit(-1)
