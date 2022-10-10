#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
from pathlib import Path
import requests
import yaml
import json
import logging
import time
import atexit
import shortuuid

from lmrtfy import _lmrtfy_profiles_dir
from lmrtfy.runner import Runner, save_json_template, RunnerStatus
from lmrtfy.runner.timer import every
from lmrtfy.login import load_token_data, LoginHandler, get_cliconfig


def send_termination(runner: Runner):
    runner.publish_runner_status(RunnerStatus.TERMINATED, "Terminated Runner")
    time.sleep(0.5)
    runner.client.loop_stop()


def send_heartbeat(runner: Runner):
    runner.publish_runner_status(runner.runner_status["status"], "Heartbeat")


def stop_heartbeat(stop_event: threading.Event, t):
    stop_event.set()
    t.join()


def main(script_path: Path, namespace: str):

    config = get_cliconfig()
    _script_path = str(Path(script_path).resolve())

    _script_identifier = _script_path.replace('/', '_').replace('\\', '_').replace('.', '_')
    _lmrtfy_profile_filename = _lmrtfy_profiles_dir.joinpath(f'{_script_identifier}.yml')

    runner_id = f"local_runner-{shortuuid.ShortUUID().random(length=9)}"

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain',
               "Authorization": f"Bearer {load_token_data()['access_token']}"}
    r = requests.post(config['api_users_url'], headers=headers,
                      data=json.dumps({'id_token': load_token_data()['id_token']}))
    logging.info(r.json())
    nickname = r.json()['nickname']

    if not namespace:
        namespace = nickname
    else:
        namespace = f"{nickname}-{namespace.replace('/','-')}"

    logging.info(namespace)

    url = config['api_catalog_url']
    try:
        with open(_lmrtfy_profile_filename, "r") as p:
            data = {"profile": yaml.safe_load(p), "namespace": namespace, "runner_id": runner_id}

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

    profile_id = None
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
        logging.debug(r.content)
        logging.error('Deployment failed.')
        exit(-1)

    r = Runner(runner_id=runner_id,
               profile_id=profile_id,
               broker_url=config['broker_url'],
               port=int(config['broker_port']),
               profile_path=_lmrtfy_profile_filename)

    stop_event = threading.Event()
    t = every(30, stop_event, send_heartbeat, r)

    atexit.register(send_termination, r)

    try:
        r.start_listening()

    except KeyboardInterrupt:
        stop_heartbeat(stop_event, t)
        exit(-1)

