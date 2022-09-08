
# Installation
There are two ways to install the lmrtfy tools. We recommend the usage of virtual environments
at the moment due to the frequent updates and changes of lmrtfy.

## Install from PyPI (recommended)
Use pip to install from PyPI:

`$ pip install lmrtfy`

This way you will always have the most recent release of the lmrtfy tools.

## Install from git
You can also install from git which is the best way to use the nightly features.

Clone the git repository and install manually:
```shell 
$ git clone --branch main https://github.com/lmrtfy/lmrtfy.git
$ cd lmrtfy
$ pip install .
```
The `main` branch is the release branch and should always work with the lmrtfy API. 

Alternatively, you can use the `develop` branch. This should be the most up-to-date branch in the
repository, but things might break. So be careful while using the `develop` branch.


# Annotate your script

The annotation of your script tells the lmrtfy tool which python variables are considered inputs and 
outputs, which is done via the `variable` and `results` functions.

This step is important, because lmrtfy traces the calls to `variable` and `result` to create a profile
for the code. This profile includes the inputs and outputs as well as the additional meta information
(`min`, `max`, `unit`, and possibly more in the future).

Let's assume that you have create a script to calculate the velocity of an object after a certain time:
```python
# file: free_fall.py
standard_gravity = 9.81
time = 200.

velocity = standard_gravity * time
print(f"Velocity after {time} seconds is {velocity} m/s.")
```

Now, if you want to recalculate for a different time, you would edit the script and run it again. While
this might work for a small script like this, this becomes tedious if you have different input variables
and want others to use your script easily, too.

Let's change the script in such a way that lmrtfy can create a profile which can be used to deploy
the function and make it available to other users:

```python
# file: free_fall_lmrtfy.py
# import the required things from lmrtfy
from lmrtfy import variable, result
standard_gravity = 9.81
# annotate an input
time = variable(200., name="time", min=0, max=1000, unit="s")

# annotate an output
velocity = result(9.81*time , name="velocity", min=0, max=9810, unit="m")
print(f"Velocity after {time} seconds is {velocity} m/s.")
```

If you run `python free_fall_lmrtfy.py` you get the exact same result as before. During the run, lmrtfy 
created the profile for `free_fall_lmrtfy.py` which will be needed to deploy the function.

## Create the annotation profile
It is required to run your script at least once with the regular python interpreter to create the
annotation profile which will be used to generate the API.
```shell
$ python <script.py>
```

The profile is currently saved under `~/.lmrtfy/profiles` which will change in the future to respect
XDG directory specifications.

## Focus: `variable` and `result`

These functions are transparent. That means the assignment `a = variable(5, name="a")` assigns `a`
the value `5`. This way you can run the script simply with your local python interpreter if lmrtfy is
installed in the environment. `variable` and `result` do not have any external dependency (e.g. API calls)

The functions signatures are as follows. Only the first two arguments are required. Ideally, the
`name` argument should match the name of the variable you assign to, although that is not necessary. 
It's considered to be a best practice, because it reduces possible errors and fosters a more intuitive 
understanding of the code.
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
  inputs are outside the specified range the job will be rejected by the generated API.
* `unit` is a `str` that declares the unit of the variable/result. This is especially useful in scientific
  calculations where units are often not standardized and unclear.



# Deploy the function (local runner)
Now you can deploy the function and make it available via the lmrtfy API. This is simply done by
```shell
$ lmrtfy deploy <path_to_script.py> --local
```
The `--local` flag means that the script will run locally on your computer and waits for jobs from
the outside. The lmrtfy API only allows job submissions that fit your deployed annotation profile.

In the future you will be able to deploy directly to the cloud. Then, you do not have to host the runner
yourself. 

The current workaround would be to use `lmrtfy` on a server or inside a docker container which can
be hosted in the cloud. 

When a job is submitted the types of the job's input parameters are checked by the lmrtfy API. Futhermore
they are also checked for their bounds and their units. This way, only jobs that can be run successfully
with the script belonging to the deployed profile. 

!!! warning
    Don't change the script after you have deployed it. The current advice would be to copy and
    rename the script before deployment. In later versions, this will be taken care of by the lmrtfy tool

# Submit a job
The lmrtfy tool also provides a way to submit jobs with the `lmrtfy` CLI tool. All you need for this 
is a `profile_id` which is provided by you during the deployment and a JSON file that contains the input
parameters.

!!! info
    Later on, you will be able to see profile_ids that are available for you on our web frontend**

For the listing above, the JSON file would look like this:
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

`argument_values` and `argument_units` contain a key-value pair each for each of the inputs in the
annotation profile. The types need to match exactly. No implicit type casting in performed during
the submission. The unit also has to match exactly.

Save the JSON file es `input.json` and run:

```shell
$ lmrtfy deploy <profile_id> input.json --local
```

!!! info
    Later on, we might perform automatic conversion in case of a unit mismatch, e.g. if the profile 
    requires `s` (as in seconds) but the input is given as `h` (as in hours). 
    
    There will be an option to enable/disable the function. If you have any opinions about that, 
    please let us know
   
When you submit your job you will receive a `job_id` which is needed to fetch the results as you
will see in the next part of this guide.

# Get results
lmrtfy also provides a way to download the results of the computation. You simply run
```shell
$ lmrtfy fetch <job_id> <save_path>
```

The `job_id` has been provided to you during the job submission. The path to save the results in is
to be specified by you. The results will be stored in JSON files inside of `<save_path>/<job_id>/`.