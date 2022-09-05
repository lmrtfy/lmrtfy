#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

from lmrtfy.login import load_token_data, LoginHandler, get_cliconfig


def fetch_results(job_id: str):
    config = get_cliconfig()
    url = config['api_results_url']

    token = ''
    # todo: login here? this isn't ideal
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
    r = requests.get(url.join(f"/{job_id}"), headers=headers)

    if r.status_code == 200:
        return r.json()
