# lmrtfy

![Linter](https://github.com/lmrtfy/lmrtfy/workflows/linter/badge.svg) [![Documentation Status](https://readthedocs.org/projects/lmrtfy/badge/?version=latest)](https://lmrtfy.readthedocs.io/en/latest/?badge=latest)

Turn variables into program arguments. Auto-generates a CLI interface and an API using lmrt.fyi.

## Introduction

lmrtfy is a tool to share your applications with others without dealing with the tedious things:

* Only minimal changes to your code by annotating your input and output variables
* Automatically generated API that can be shared with others

!!! warning
lmrtfy is currently in an early alpha phase. We try to minimize the things that will change in
the future, but we cannot make any guarantees at the moment. Please keep that in mind while using
the lmrtfy tools.

Currently, the application itself runs on your computer and we provide a tightly controlled interface
via our web API to start jobs that make use of the script running on your computer. Follow the quick
start guide to get started!

We also have a more comprehensive [guide](guide.md) and [examples](examples.md) that you might be interested in!

!!! Note
If you encounter any obstacles while using our tool or while reading the documentation, please don't
hesitate to contact us. Just create an issue on GitHub.

## Quickstart

### TL;DR
1. intall with `pip install lmrtfy`
2. login/sign up with `lmrtfy login`
3. annotate your code's inputs with `variable` and its outputs with `result`
4. in terminal 1 run `lmrtfy deploy <script.py> --local` (returns profile_id)
5. in terminal 2 run `lmrtfy submit <profile_id> <input.json>` (returns job_id)
6. in terminal 2 run `lmrtfy fetch <job_id> <path>` to get results

### Installation:
`$ pip install lmrtfy`

### First login
Login/sign up to receive access token: `$ lmrtfy login`. The token is saved in `~/.lmrtfy/auth/token` but you
should not need to manually open the token.


!!! info
Tokens are currently valid for 24 hours. After that you will be requested to login again. That also means
that you cannot have scripts deployed more than 24 hours right now. This will change soon so that you
can deploy scripts longer than that.

    Just run `lmrtfy deploy <script> --local`again after 24h and you are fine if you need longer running
    deployments right now.)

### Create code annotations
Annotate the inputs and outputs of your script with `variable` and `results` and save it as `script.py`:
```python
# import the required things from lmrtfy
from lmrtfy import variable, result
# annotate an input
time = variable(200., name="time", min=0, max=1000, unit="s")
speed = result(9.81*time, name="speed", min=0, max=9810, unit="m/s")
```

This calculates the velocity of an object in free fall after `time` seconds.

Run `python script.py` to create the profile. This **always** works, even without access to lmrtfy.

### Deploy the script to accept jobs from the generated web API
Run `lmrtfy deploy script.py --local` to generate the API and start the runner to listen to jobs for your script.
You can find the profile id to submit a job in the logs:
```shell
INFO Starting deployment of examples/velocity_from_gravity/calc_velocity.py
WARNING Deploying locally.
INFO Profile_id to be used for requests: 7ff68a0cfd8c61122cfdaf0a835c7cd1f94e7db9
```

### Submit jobs with CLI
Open a new terminal and submit a new job (`<profile_id>` is the profile id you received during the deployment (`7ff...` in the example above)):
```shell
$ lmrtfy submit <profile_id> <input.json>
```
For the example above save the following in your `input.json`:
```json
{
  "argument_values": {
    "time": 200.0
  },
  "argument_units" : {
    "time": "s"
  }
}
```
You will receive a `job_id` which you will need to fetch the results later on:
```shell
INFO Job-id: 14584640-778c-4f91-a288-03cffc2b9c7a
```
### Fetch results
Get the results by calling `$ lmrtfy fetch <job_id> <path>`. Currently, the results will be saved
in `<path>/<job_id>` as JSON files. 

# License
![BSD 3-Clause License](https://github.com/lmrtfy/lmrtfy/blob/main/LICENSE)
