#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import hashlib
import json
import requests
import secrets
import threading
import urllib
import webbrowser
from time import sleep
import jwt
from flask import Flask, request
from werkzeug.serving import make_server
from lmrtfy import _lmrtfy_auth_dir
from typing import Optional


def get_cliconfig():
    r = requests.get('https://api.simulai.de/cliconfig')
    return r.json()


def auth_url_encode(byte_data):
    return base64.urlsafe_b64encode(byte_data).decode('utf-8').replace('=', '')


def generate_challenge(a_verifier):
    return auth_url_encode(hashlib.sha256(a_verifier.encode()).digest())


def save_token_data(token_data):

    try:
        with open(_lmrtfy_auth_dir.joinpath('token'), 'w') as f:
            json.dump(token_data, f)
    except:
        pass


def load_token_data() -> Optional[dict]:

    try:
        with open(_lmrtfy_auth_dir.joinpath('token'), 'r') as f:
            return json.load(f)
    except:
        return {'access_token':'', 'id_token':'', 'refresh_token':''}


class ServerThread(threading.Thread):

    def __init__(self, app, host: str, port: int):
        threading.Thread.__init__(self)
        self.srv = make_server(host, port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()


class LoginHandler(object):
    def __init__(self):

        self.cliconfig = get_cliconfig()

        self.received_callback = False
        self.code = None
        self.error_message = None
        self.received_state = None

        self.verifier = auth_url_encode(secrets.token_bytes(32))
        self.redirect_uri = f"http://{self.cliconfig['auth_listener_host']}:{self.cliconfig['auth_listener_ports'][0]}/callback"

    def callback(self):
        # TODO: Make this look nice.
        message = "Success"
        if 'error' in request.args:
            self.error_message = request.args['error'] + ': ' + request.args['error_description']
            message = "Error"
        else:
            self.code = request.args['code']

        self.received_state = request.args['state']
        self.received_callback = True

        return f"<center><h1>{message}. Please return to your application now.</h1></center>"

    def login(self):

        if self.token_is_valid(load_token_data()['access_token']):
            return False

        challenge = generate_challenge(self.verifier)
        state = auth_url_encode(secrets.token_bytes(32))

        app = Flask("LMRTFY Login")

        @app.route('/callback')
        def callback():
            return self.callback()

        server = ServerThread(app, self.cliconfig['auth_listener_host'], int(self.cliconfig['auth_listener_ports'][0]))
        server.start()

        base_url = f"{self.cliconfig['auth_authorize_url']}?"
        url_parameters = {
            'audience': self.cliconfig['auth_audience'],
            'scope': "profile openid offline_access",  #self.cliconfig['auth_scopes'],
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'client_id': self.cliconfig['auth_client_id'],
            'code_challenge': challenge.replace('=', ''),
            'code_challenge_method': 'S256',
            'state': state
            }

        url = base_url + urllib.parse.urlencode(url_parameters)
        webbrowser.open_new(url)

        while not self.received_callback:
            sleep(1)

        server.shutdown()

        if state != self.received_state:
            print("Error: session replay or similar attack in progress. Please log out of all connections.")
            exit(-1)

        if self.error_message:
            print("An error occurred:")
            print(self.error_message)
            exit(-1)

        return True

    def get_token(self):
        headers = {'Content-Type': 'application/json'}
        body = {'grant_type': 'authorization_code',
                'client_id': self.cliconfig['auth_client_id'],
                'code_verifier': self.verifier,
                'code': self.code,
                'audience': self.cliconfig['auth_audience'],
                'redirect_uri': self.redirect_uri}
        r = requests.post(self.cliconfig['auth_token_url'], headers=headers, data=json.dumps(body))
        data = r.json()

        if self.token_is_valid(data['access_token']):
            save_token_data(data)

    def token_is_valid(self, token) -> bool:

        if not token:
            return False

        try:
            r = requests.get(self.cliconfig['auth_jwks_url'])
            jwks = r.json()
            public_keys = dict()

            for jwk in jwks['keys']:
                kid = jwk['kid']
                public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

            kid = jwt.get_unverified_header(token)['kid']
            jwt.decode(token, key=public_keys[kid], algorithms=["RS256"], audience=self.cliconfig['auth_audience'], verify=True)

            return True

        except Exception:
            pass

        return False


