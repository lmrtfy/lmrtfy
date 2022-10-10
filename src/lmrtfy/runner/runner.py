# -*- coding: utf-8 -*-
import enum
import json
import logging
import os
import pathlib
import queue
import subprocess
import tempfile
import time
import uuid
from typing import Optional

import certifi
import jwt
import paho.mqtt.client as mqtt
import requests
import yaml

from lmrtfy.helper import NumpyEncoder
from lmrtfy.login import load_token_data, get_cliconfig
from lmrtfy.runner.timer import every

class RunnerStatus(str, enum.Enum):
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    TERMINATED = "TERMINATED"


class JobStatus(str, enum.Enum):
    UNKNOWN = "UNKNOWN"
    ACCEPTED = "ACCEPTED"
    RUNNING = "RUNNING"
    REJECTED = "REJECTED"
    FAILED = "FAILED"
    RESULTS_READY = "RESULTS_READY"
    SUBMITTED = "SUBMITTED"


def on_mqtt_disconnect(client, userdata, flags, rc, properties=None):
    logging.debug("on_disconnect")
    logging.debug(f"  userdata  : {userdata}")
    logging.debug(f"  flags     : {flags}")
    logging.debug(f"  rc        : {rc}")
    logging.debug(f"  properties: {properties}")

    logging.warning("Disconnected from MQTT broker.")


def on_subscribe(client, userdata, flags, rc, properties=None):
    logging.debug("on_subscribe")
    logging.debug(f"  userdata  : {userdata}")
    logging.debug(f"  flags     : {flags}")
    logging.debug(f"  rc        : {[x.getName() for x in rc]}")
    logging.debug(f"  properties: {properties}")




class Runner(object):
    """
    The Runner class is responsible for listening to incoming jobs and the execution of the
    underlying profile with the
    parameters of the incoming jobs.

    Jobs are managed in a queue.

    The Runner sends status messages into a dedicated topic for this specific client.

    :param broker_url: MQTT broker url
    :type broker_url: str
    :param port: Port to use for MQTT
    :type port: int
    :param profile_path: Path to the user-profile that the runner is connected to
    :type profile_path: pathlib.Path
    """

    def __init__(self, runner_id: str, profile_id: str, broker_url: str, port: int, profile_path: pathlib.Path):
        """
        Constructor method
        """
        self.job_list = queue.Queue()
        self.busy = False

        # TODO: test if profile is available
        with open(profile_path, "r") as p:
            self.profile = yaml.safe_load(p)

        logging.debug(self.profile)

        self.filehash = self.profile["filehash"]
        logging.debug(f"Running for profile-id: {self.filehash}")

        # TODO: client id is ideally the same a the filehash I guess. Issue #6
        self.client_id = runner_id
        self.profile_id = profile_id
        # TODO: runner status => Load, RAM Status, ...
        self.runner_status_topic = f"status/runner/{self.client_id}"
        self.heartbeat_topic = f"heartbeat/runner/{self.client_id}"
        self.job_status_topic = f"status/job/"
        # TODO: second status topic for job status

        access_token = load_token_data()['access_token']
        user_id = jwt.decode(access_token, options={"verify_signature": False})["sub"]
        self.user_id = user_id.replace('|','-----')
        # job_topic =  f"$share/{user_id}/{user_id}/{self.filehash}/job"
        # self.client.subscribe(job_topic, qos=2)

        self.client = mqtt.Client(
            client_id=self.client_id,
            protocol=mqtt.MQTTv5,
            transport="websockets"
        )

        access_token = ''
        try:
            access_token = load_token_data()['access_token']
        except Exception:
            # Todo: give error
            pass

        self.client.tls_set(certifi.where())
        # self.client.enable_logger()
        self.client.username_pw_set(self.client_id, access_token)
        self.client.on_connect = self.on_mqtt_connect
        self.client.on_disconnect = on_mqtt_disconnect
        self.client.on_subscribe = on_subscribe

        # keepalive need to be below the time out of the server (mosquitto => 60s default)
        self.client.connect(broker_url, port, keepalive=30)

        # TODO: how to structure shared-groups and topics?

        self.client.loop_start()
        time.sleep(1)

        self.job_status = {
            "filehash": self.filehash,
            "job_id": None,
            "status": JobStatus.UNKNOWN,
            "message": "",
        }
        self.runner_status = {
            "filehash": self.filehash,
            "runner_id": self.client_id,
            "status": RunnerStatus.IDLE,
            "message": "",
        }

        self.publish_runner_status(RunnerStatus.IDLE, "Started idling.")

    def on_mqtt_connect(self, client, userdata, flags, rc, properties=None):
        logging.debug("on_connect")
        logging.debug(f"  userdata  : {userdata}")
        logging.debug(f"  flags     : {flags}")
        logging.debug(f"  rc        : {rc}")
        logging.debug(f"  properties: {properties}")
        if rc == 0:
            logging.info("Successfully connected to MQTT broker.")

        job_topic = f"$share/{self.user_id}/{self.profile_id}/{self.filehash}"
        self.client.subscribe(job_topic)
        logging.debug(f"Listen for jobs on '{job_topic}'.")

    def on_message(self, client, userdate, msg):
        """
        on_message is a callback for the MQTT client which is executed everytime a message is
        received.
        There are two steps:
            1. publish a status message that a job has been received
            2. add the job to the job queue of the runner class for later execution
        """
        logging.debug("on_message")
        logging.debug(f"  userdate: {userdate}")
        logging.debug(f"  msg: {msg}")
        job = json.loads(msg.payload)
        self.job_list.put(job, block=False)
        self.publish_job_status(JobStatus.ACCEPTED, "Accepted job", job["user_id"], json.loads(msg.payload)["job_id"])

    def publish_job_status(self, status: JobStatus, message: str, user_id: str, job_id: Optional[str] = None):
        """
        Publishes a status message with JobStatus and a message to MQTT.

        :param status: One of the available job stati for job monitoring.
        :type status: JobStatus
        :param message: A human-readable message.
        :type message: str
        :param job_id: job_id for the status message. Does not always apply. default: None
        :type job_id: Optional[int]
        """
        # TODO: Why is job_status a class member?
        self.job_status["status"] = status
        self.job_status["message"] = message
        self.job_status["job_id"] = job_id
        self.job_status["user_id"] = user_id

        job_status_topic = f"status/job/{job_id}"
        logging.info(
            f"status update for job '{job_id}': '{status}' with '{message}' for "
            f"profile-id '{self.filehash}' and client-id `{self.client_id}`."
        )
        self.client.publish(job_status_topic, json.dumps(self.job_status))

    def publish_runner_status(self, status: RunnerStatus, message: str):
        if message != "Heartbeat":
            logging.info(f"status update for runner `{self.client_id}: '{status}' with '{message}'.")
        else:
            logging.debug(f"status update for runner `{self.client_id}: '{status}' with '{message}'.")

        self.runner_status["user_id"] = self.user_id
        self.runner_status["status"] = status
        self.runner_status["message"] = message
        self.client.publish(self.runner_status_topic, json.dumps(self.runner_status))


    def execute(self, job_id: str, user_id: str, job_input: dict):
        """
        `execute` is responsible for the actual execution of the command with the correct input
        parameters.

        :param job_id:
        :param job_input:
        """

        config = get_cliconfig()
        command = self.profile["language"]
        if "python" not in command:
            logging.error(f"{command} is currently not supported.")

        script = self.profile["filename"]

        # TODO: Techdebt. Ignoring the cleanup errors is due to a python uptream bug in tempfile. bugs.python.org #43153
        try:
            tempdir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)  # pylint: disable=consider-using-with
        except:
            tempdir = tempfile.TemporaryDirectory()  # pylint: disable=consider-using-with
        # TODO: Add job_id to path
        os.environ["LMRTFY_TMP_DIR"] = tempdir.name
        logging.debug(f"Set LMRTFY_TMP_DIR to '{tempdir.name}'.")

        # Set write input files
        for var, meta_data in self.profile["variables"].items():
            var_path = pathlib.Path(tempdir.name).joinpath(f"lmrtfy_variable_{var}.json")
            with open(var_path, "w") as input_file:
                json.dump({var: job_input[var]}, input_file, cls=NumpyEncoder)

            logging.debug(f"Created '{str(var_path)}' with expected type '{meta_data['dtype']}'.")
            logging.debug(f"  Set to: '{job_input[var]}'")

        command_args_list = [command, script]
        logging.info(f"Running the follow command: {command_args_list}")

        # Set environment variables for execution and run code
        # TODO: How safe is that?
        self.publish_job_status(JobStatus.RUNNING, "Running script.", user_id=user_id, job_id=job_id)
        os.environ["LMRTFY_DEPLOY_LOCAL"] = "1"
        result_code = subprocess.run(command_args_list, capture_output=True)

        # check results
        if result_code.returncode != 0:
            self.publish_job_status(JobStatus.FAILED, "FAILED!", user_id=user_id, job_id=job_id)
            logging.error("Execution failed for some reason.")
            logging.error(f"stderr: \n {result_code.stderr.decode()}")
        else:
            logging.debug("Execution succeeded.")
            logging.debug(f"stdout of execution: {result_code.stdout.decode()}")

        results = {}
        failed = False
        for res, meta_data in self.profile["results"].items():
            res_path = pathlib.Path(tempdir.name).joinpath(f"lmrtfy_result_{res}.json")
            try:
                with open(res_path, "r") as result_file:
                    results[res] = json.load(result_file)
                    # TODO: add auth code, change results endpoint!
                    files = {'results_file': open(res_path, 'rb')}

                    try:
                        token = load_token_data()['access_token']
                        headers = {"Authorization": f"Bearer {token}"}
                    except Exception:
                        # TODO: Fix exception and log meaningful error message
                        pass

                    r = requests.post(f"{config['api_results_url']}/{user_id}/{job_id}", files=files,
                                      headers=headers)
                    logging.debug(r)
                    if r.status_code != 200:
                        logging.error("Results could not be uploaded")
                        failed = True
            except FileNotFoundError:
                failed = True
                logging.error(f"Result file '{res_path}' not found.")
                break

        if failed:
            self.publish_job_status(JobStatus.FAILED, "Job failed.", user_id, job_id=job_id)
        else:
            self.publish_job_status(JobStatus.RESULTS_READY, "Results ready.", user_id, job_id=job_id)

        logging.debug(results)

        try:
            tempdir.cleanup()
        except:
            pass

        self.busy = False

    def start_listening(self):
        """
        This method waits for arriving jobs and starts the execution.
        """
        self.client.on_message = self.on_message
        #try:
        # queue.get() blocks until an element is inside the queue.
        # This might not work on Windows which has to be tested
        while True:
            # time.sleep(0.1)
            # TODO: this check might be necessary on windows... if not self.job_list.empty()
            #  and not self.busy:
            # if not self.job_list.empty() and not self.busy:
            # self.busy = True
            self.publish_runner_status(RunnerStatus.IDLE, "Waiting for job in MQTT Topic.")

            # blocks until something is in the queue
            job_id, user_id, _, job_param, _, _ = self.job_list.get().values()
            self.publish_runner_status(RunnerStatus.RUNNING, "Starting execution.")
            logging.debug(f"'{job_param}' for job_id '{job_id}'")
            self.execute(job_id, user_id, job_param)
            self.job_list.task_done()
        #except KeyboardInterrupt:
        #    logging.info("Detected KeyboardInterrupt. Stop program.")
        #    self.client.loop_stop()
        #    exit(-1)
