# Installation: 

We provide a [PyPI package](https://pypi.org/project/lmrtfy/)

!!! note
    We recommend installing LMRTFY into a virtual environment to keep your system clean.

## Linux and MacOS
We provide a PyPI package for Linux and MacOS which can be installed easily with `pip`:

```shell
$ pip install lmrtfy
```

## Windows
On Windows the `conda` package manager provided by 
[miniconda and Anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html)
is the best way to use Python and install Python packages.

Right now, we only support a PyPI package which can be installed with `conda`. If you have `pip` installed
in your conda environment you can directly install from PyPI, otherwise you need to install `pip` first:
```shell
$ conda install pip
$ pip install lmrtfy
```

# First login 

Login/sign up to receive access token: `$ lmrtfy login`. The token is saved in `~/.lmrtfy/auth/token` but you 
should not need to manually open the token.


# Create code annotations
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

# Deploy the script to accept jobs from the generated web API
Run `lmrtfy deploy script.py --local` to generate the API and start the runner to listen to jobs for your script. 
You can find the profile id to submit a job in the logs: 
```shell
INFO Starting deployment of examples/velocity_from_gravity/calc_velocity.py
WARNING Deploying locally.
INFO Profile_id to be used for requests: 7ff68a0cfd8c61122cfdaf0a835c7cd1f94e7db9
```

# Submit jobs with CLI
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
# Fetch results
Get the results by calling `$ lmrtfy fetch <job_id> <path>`. Currently, the results will be saved 
in `<path>/<job_id>` as JSON files. 



