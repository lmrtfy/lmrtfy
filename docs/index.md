# Welcome to lmrtfy

This is the official documentation of the lmrtfy project!

---

**Note:**

** lmrtfy is currently in an early alpha phase. We try to minimize the things that will change in
the future but we cannot make any guarantees at the moment. Please keep that in mind while using
the lmrtfy tools.**

---

lmrtfy is a tool to share your applications with others without dealing with the tedious things:

* Only minimal changes to your code by annotating your input and output variables
* Automatically generated API that can be shared with others

# Quickstart
* Installation: `pip install lmrtfy`
* Annotate the inputs and outputs of your script with `variable` and `results`:
```python
# import the required things from lmrtfy
from lmrtfy import variable, result
# annotate an input
time = variable(200., name="time", min=0, max=1000, unit="s")
speed = result(9.81*time, name="speed", min=0, max=9810, unit="m/s")
```

This calculates the velocity of an object in free fall after `time` seconds.

* Run `python <script.py>` to create profile. 
* Run `lmrtfy deploy <script.py> --local` to generate the API and start the runner to listen to jobs for your script. 
You can find the profile id to submit a job in the logs: 
```shell
2022-09-05 11:07:15 [31031] INFO Starting deployment of examples/velocity_from_gravity/calc_velocity.py
2022-09-05 11:07:15 [31031] WARNING Deploying locally.
2022-09-05 11:07:16 [31031] INFO Profile_id to be used for requests: 7ff68a0cfd8c61122cfdaf0a835c7cd1f94e7db9
```

* Now, you can submit a job with curl:
```shell
curl --location --request POST 'https://api.simulai.de/y/<profile_id>' \
--header 'Authorization: Bearer <access token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "profile_id": "<profile_id>",
    "job_parameters": {
            "time": 50.0
    },
    "parameter_units": {
			"time": "s"
		}
}'
```
The access token can be found in `~/.lmrtfy/auth/token` (json file) with the key `access_token".

**Note: Job submission will become more comfortable in later releases**

# Guide
## Installation
There are two ways to install the lmrtfy tools. We recommend the usage of virtual environments
at the moment due to the frequent updates and changes of lmrtfy.

### Install from PyPI (recommended)
Use pip to install from PyPI: 

`pip install lmrtfy`

This way you will always have the most recent release of the lmrtfy tools.

### Install from git
You can also install from git which is the best way to use the nightly features. 

Clone the git repository and install manually:
```shell 
$ git clone https://github.com/lmrtfy/lmrtfy.git
$ cd lmrtfy
$ pip install .
```

## Annotate your script

The annotation of your script tells the lmrtfy tool which variables are considered inputs and outputs.

This is done via the `variable` and `results` functions:
```python
# import the required things from lmrtfy
from lmrtfy import variable, result
# annotate an input
input1 = variable(200., name="input1", min=0, max=1000, unit="s")
output1 = result(9.81*input1, name="output1", min=0, max=9810, unit="m")
```

The function signatures are as follows. Only the first two arguments are required.
```python
# variable signature:
variable(value: supported_object_type, 
         name: str, 
         min = None, max = None, 
         unit: str = None) -> supported_object_type
# result signature:
result(value: supported_object_type,
        name: str,
        min = None, max = None,
        unit: str = None) -> supported_object_type
```
* The `value` argument specifies the default argument for the variable and has to be one of the 
supported types: `int, float, complex, bool, np.ndarray, list, dict`. 
* `name` declares the name of the variable that will be used for the API generation. A sensible choice
is the same name as the variable's name in the code itself.
* `min` and `max` can be used to specify boundaries for the input and output values in case they are
numeric. This might come in handy if the code only works for certain input parameter ranges. If the
inputs are outside of the specified range the job will be rejected by the generated API.
* `unit` is a `str` that declares the unit of the variable/result. This is especially useful in scientific
calculations where units are often not standardized and unclear.

## Create the annotation profile
It is required to run your script at least once with the regular python interpreter to create the
annotation profile which will be used to generate the API.
```shell
$ python <script.py>
```

The profile is currently saved under `~/.lmrtfy/profiles` which will change in the future to respect
XDG directory specifications. 

## Deploy the function (local runner)
Now you can deploy the function and make it available via the lmrtfy API. This is simply done by
```shell
$ lmrtfy deploy <path_to_script.py> --local
```
The `--local` flag means that the script will run locally on your computer and waits for jobs from 
the outside. 

# Example
This is a simple example to showcase how to use the lmrtfy tools. It can be found in `examples/example1/example1.py`
```python
import numpy as np
from lmrtfy import variable, result


x = variable(5, name="x", min=1, max=10)
y = variable(np.linspace(0., 1., 101, dtype=np.float64), name="y", min=-1., max=11., unit="m")
z = variable("abc", name="z")

z1 = variable(["abc", "def"], name="z1")
z2 = variable(["abc", 1, 1.1], name="z2")
z3 = variable({'a': "abc", 'b': 1}, name="z3")

a = result(x * y, name="a")
b = result(x * z, name="b")
```

1. Run `python examples/example1/example1.py`. This will create the deployment profile for you.
2. Next, run `lmrtfy deploy examples/example1/example1.py` to make the script accessible for others via API.

