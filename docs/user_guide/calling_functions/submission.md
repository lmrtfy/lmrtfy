## Calling a function from code
Our goal is to provide an interface to deployed functions that works just like any other function in 
any other library that you have locally installed.

We provide an example `call_free_fall.py` in the same directory as the `free_fall_lmrtfy.py`
script. 

As you can see, calling a remote function via LMRTFY feels just like calling a native function.

```py title="call_free_fall.py" linenums="1"
from time import sleep
from lmrtfy import catalog  # (1)!

job = catalog.examples.free_fall_lmrtfy(time=100.) # (2)!

if job:
    print(job.id, job.status)
    
    while not job.ready: # (3)!
        sleep(1.)
    
    print(job.results) # (4)!
```

1. Importing the catalog triggers the catalog update to get newly deployed functions every time you
run the code. Our examples are all part of the catalog in the `catalog.examples` namespace.
2. The function `free_fall_lmrtfy` is now part of the catalog and can be called just like a
normal function in your code. The function is not executed in the same context as your Python
interpreter. Instead it is run in one of the runners.
3. Loop until the job is ready. In this context `ready` means that the results are ready to be fetched.
4. Fetching the results is as simple as calling `job.results`. The return value is a dictionary with the keys
corresponding to the names of the results and the values are the actual values of the result

Run the script with your local python interpreter `#!shell python call_free_fall.py`. It runs just
like a regular script but calls a remote function inside. 

The output of the script looks like this:
```shell 
INFO Validating auth token.
INFO Auth token accepted.
INFO Valid access token found. Login not necessary.
INFO Updated function catalog.
INFO Added function free_fall_lmrtfy.
INFO Job CLuz1ZrpR7 created. Status is RUNNING. # (1)!
CLuz1ZrpR7 JobStatus.RUNNING
{'velocity': 981.0} # (2)!
```

1. The job ID is always a 10-character long ID. The reported status is sometimes UNKNOWN which usually
means that the LMRTFY platform has not processed the job yet.
2. The result of the computation is a dictionary with the variable names as keys and the actual value
as values.

The ID of the job is going to be different from the one shown in the example output. Job IDs are
always 10 characters long.

## Using the CLI

LMRTFY also provides a way to submit jobs with the `lmrtfy` CLI tool. All you need for this
is a `profile_id` (7 characters long) which is provided by you during the deployment and a 
JSON file that contains the input parameters.

!!! attention
    This is a good way to call deployed scripts from another language as you can always build the
    JSON file and call the `lmrtfy` CLI. **If you are using it this way, please contact us. We want to
    provide more native-feeling interfaces to languages other than python as well but would love to 
    hear what you use to prioritize.**

For the example calculating the compound interest, the JSON file would look like this:
```json
{
  "argument_values": {
    "time": 100
  },
  "argument_units": {
    "time": "s"
  }
}

```

`argument_values` and `argument_units` contain a key-value pair each for each of the inputs in the
annotation profile. The types need to match exactly. No implicit type casting in performed during
the submission. The unit also has to match exactly.

Save the JSON file es `input.json` and run:

```shell
$ lmrtfy submit <profile_id> input.json
```

!!! info
    Later on, we might perform automatic conversion in case of a unit mismatch, e.g. if the profile
    requires `s` (as in seconds) but the input is given as `h` (as in hours).

    There will be an option to enable/disable the function. If you have any opinions about that, 
    please let us know

When you submit your job you will receive a `job_id` which is needed to fetch the results as you
will see in the next part of this guide.
