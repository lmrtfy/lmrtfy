# -*- coding: utf-8 -*-
import logging
import os
import time
import json
import uuid
import subprocess
import tempfile
import pathlib
import enum
import queue
from typing import Optional

import yaml
import paho.mqtt.client as mqtt

from lmrtfy.annotation import NumpyEncoder


class JobStatus(str, enum.Enum):
    IDLE = "IDLE"
    WAITING = "WAITING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    JOB_RECEIVED = "JOB_RECEIVED"
    RUNNING = "RUNNING"
    RESULTS_READY = "RESULTS_READY"
    INCOMPLETE_RESULTS = "INCOMPLETE_RESULTS"
    ABORTED = "ABORTED"


def on_mqtt_connect(client, userdata, flags, rc, properties=None):
    logging.debug("on_connect")
    logging.debug(f"  userdata  : {userdata}")
    logging.debug(f"  flags     : {flags}")
    logging.debug(f"  rc        : {rc}")
    logging.debug(f"  properties: {properties}")
    if rc == 0:
        logging.info("Successfully connected to MQTT broker.")


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
    :param username: username for MQTT broker
    :type username: str
    :param password: password for MQTT broker
    :type password: str
    :param profile_path: Path to the user-profile that the runner is connected to
    :type profile_path: pathlib.Path
    """

    def __init__(self, broker_url, port, username, password, profile_path):
        """
        Constructor method
        """
        self.job_list = queue.Queue()
        self.busy = False

        with open(profile_path, "r") as p:
            self.profile = yaml.safe_load(p)

        logging.debug(self.profile)

        self.filehash = self.profile["filehash"]
        logging.debug(f"Running for filehash: {self.filehash}")

        # TODO: client id is ideally the same a the filehash I guess. Issue #6
        self.client_id = f"local_runner-{uuid.uuid4()}"
        self.status_topic = f"status/{self.client_id}"

        self.client = mqtt.Client(
            client_id=self.client_id, protocol=mqtt.MQTTv5, transport="websockets"
        )
        self.client.tls_set()
        # self.client.enable_logger()
        self.client.username_pw_set(username, password)
        self.client.on_connect = on_mqtt_connect
        self.client.on_disconnect = on_mqtt_disconnect
        self.client.on_subscribe = on_subscribe

        # keepalive need to be below the time out of the server (mosquitto => 60s default)
        self.client.connect(broker_url, port, keepalive=30)
        # TODO: how to structure shared-groups and topics?
        self.client.subscribe(f"$share/{self.filehash}/{self.filehash}/job", qos=2)
        self.client.loop_start()
        time.sleep(1)

        self.status = {
            "filehash": self.filehash,
            "job_id": None,
            "status": JobStatus.IDLE,
            "message": "",
        }
        self.publish_status(JobStatus.IDLE, "Started idling.")

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
        self.publish_status(JobStatus.JOB_RECEIVED, "Received job")
        self.job_list.put(json.loads(msg.payload), block=False)

    def publish_status(self, status: JobStatus, message: str, job_id: Optional[int] = None):
        """
        Publishes a status message with JobStatus and a message to MQTT.

        :param status: One of the available job stati for job monitoring.
        :type status: JobStatus
        :param message: A human-readable message.
        :type message: str
        :param job_id: job_id for the status message. Does not always apply. default: None
        :type job_id: Optional[int]
        """
        self.status["status"] = status
        self.status["message"] = message
        self.status["job_id"] = job_id
        if job_id:
            logging.info(
                f"status update for job '{job_id}': '{status}' with '{message}' for "
                f"filehash '{self.filehash}' and client-id `{self.client_id}`."
            )
        else:
            logging.info(
                f"status update: '{status}' with '{message}' for filehash "
                f"'{self.filehash}' and client-id `{self.client_id}`."
            )

        self.client.publish(self.status_topic, json.dumps(self.status))

    def execute(self, job_id: int, job_input: dict):
        """
        `execute` is responsible for the actual execution of the command with the correct input
        parameters.

        :param job_input:
        """
        command = self.profile["language"]
        if "python" not in command:
            logging.error(f"{command} is currently not supported.")

        script = self.profile["filename"]

        tempdir = tempfile.TemporaryDirectory()  # pylint: disable=consider-using-with
        os.environ["LMRTFY_TMP_DIR"] = tempdir.name
        logging.debug(f"Set LMRTFY_TMP_DIR to '{tempdir.name}'.")

        self.publish_status(JobStatus.RUNNING, "Reading input variables.", job_id=job_id)
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
        self.publish_status(JobStatus.RUNNING, "Running script.", job_id=job_id)
        os.environ["LMRTFY_DEPLOY_LOCAL"] = "1"
        result_code = subprocess.run(command_args_list, capture_output=True)

        # check results
        if result_code.returncode != 0:
            self.publish_status(JobStatus.FAILED, "FAILED!", job_id=job_id)
            logging.error("Execution failed for some reason.")
            logging.error(f"stderr: \n {result_code.stderr.decode()}")
        else:
            self.publish_status(JobStatus.SUCCESS, "SUCCESS", job_id=job_id)
            logging.debug("Execution succeeded.")
            logging.debug(f"stdout of execution: {result_code.stdout.decode()}")

        results = {}
        partial_results_only = False
        for res, meta_data in self.profile["results"].items():
            res_path = pathlib.Path(tempdir.name).joinpath(f"lmrtfy_result_{res}.json")
            try:
                with open(res_path, "r") as result_file:
                    results[res] = json.load(result_file)
            except FileNotFoundError:
                partial_results_only = True
                logging.error(f"Result file '{res_path}' not found.")

        # TODO: results handler => what to do with results

        if partial_results_only:
            self.publish_status(
                JobStatus.INCOMPLETE_RESULTS, "Partial results available", job_id=job_id
            )
        else:
            self.publish_status(
                JobStatus.RESULTS_READY, "Results are ready for download", job_id=job_id
            )
        logging.debug(results)
        self.busy = False

    def start_listening(self):
        """
        This method waits for arriving jobs and starts the execution.
        """
        self.client.on_message = self.on_message
        try:
            # TODO: ISSUE #9 -> this could possibly be one of the drivers of high loads
            # queue.get() blocks until an element is inside the queue.
            # This might not work on windows which has to be tested
            while True:
                # time.sleep(0.1)
                # TODO: this check might be necessary on windows... if not self.job_list.empty()
                #  and not self.busy:
                # if not self.job_list.empty() and not self.busy:
                # self.busy = True
                self.publish_status(JobStatus.WAITING, "Waiting for Job in MQTT Topic.")

                # blocks until something is in the queue
                job_id, job_param = self.job_list.get().values()
                self.publish_status(JobStatus.RUNNING, "Starting execution.")
                logging.debug(f"'{job_param}' for job_id '{job_id}'")
                self.execute(job_id, job_param)
                self.job_list.task_done()
                self.publish_status(JobStatus.IDLE, "Back to Idle.")
        except KeyboardInterrupt:
            logging.info("Detected KeyboardInterrupt. Stop program.")
            self.client.loop_stop()
