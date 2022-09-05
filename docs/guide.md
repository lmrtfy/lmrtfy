
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
the outside. The lmrtfy API only allows job submissions that fit your deployed annotation profile.

The inputs are type checked and also checked for their valid ranges and units. Only jobs that can run 
successfully with your code reach your code at all. 

## Submit a job
The lmrtfy tool also provides a way to submit jobs with the `lmrtfy` CLI tool. All you need for this 
is a `profile_id` which is provided by you during the deployment and a json-file that contains the input
parameters.

**Note: Later on, you will be able to see profile_ids that are available for you on our web frontend**

For the listing above, the json file would look like this:
```json
{
  "profile_id": "<profile_id>",
  "job_parameters": {
    "time": 200.0
  },
  "parameter_units" : {
    "time": "s"
  }
}
```

`profile_id` needs to be specified inside the json as well, which is a slight inconvenience at the 
moment, but allows us to be more flexible later on. 

`job_parameters` and `parameter_units` contain a key-value pair each for each of the inputs in the 
annotation profile. The types need to match exactly. No implicit type casting in performed during
the submission. The unit also has to match exactly. 

_Later on, we might perform automatic conversion
in case of a unit mismatch, e.g. if the profile requires `s` (as in seconds) but the input is given
as `h` (as in hours)._

When you submit your job you will receive a `job_id` which is needed to fetch the results as you
will see in the next part of this guide.

## Get results
lmrtfy also provides a way to download the results of the computation. You simply run
```shell
$ lmrtfy fetch <job_id> <save_path>
```

The `job_id` has been provided to you during the job submission. The path to save the results in is
to be specified by you. The results will be stored in JSON files inside of `<save_path>/<job_id>/`.