#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import hashlib
import json
import os
import pathlib
import requests
import secrets
import threading
import urllib
import webbrowser
from time import sleep
import jwt
import flask
from flask import Flask, request

from werkzeug.serving import make_server


def get_cliconfig():
    r = requests.get('http://api.simulai.de/cliconfig')
    return r.json()


def auth_url_encode(byte_data):
    return base64.urlsafe_b64encode(byte_data).decode('utf-8').replace('=', '')


def generate_challenge(a_verifier):
    return auth_url_encode(hashlib.sha256(a_verifier.encode()).digest())


def save_token_data(token_data):
    pass


def load_token_data():
    pass


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
        """
        The callback is invoked after a completed login attempt (successful or otherwise).
        It sets global variables with the auth code or error messages, then sets the
        polling flag received_callback.
        :return:
        """
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

        if self.token_is_valid():
            return

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
        save_token_data(data)
        print(data)

    def token_is_valid(self):
        token_data = load_token_data()
        # Check validity and expiration
        return False


