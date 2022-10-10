# Calling a Deployed Function

Let's assume that you have just deployed the script `calc_compound_interest.py` from the examples 
provided in `examples/compound_interest/calc_compound_interest.py` by running

```shell
$ lmrtfy deploy examples/compound_interest/calc_compound_interest.py --local
```

Do not close that terminal as there won't be a runner to receive jobs in that case.

## Calling a Function from Code
Our goal is to provide an interface to deployed functions that works just like any other function in 
any other library that you have locally installed.

We provide an example `call_compound_interest.py' in the same directory as the `calc_compound_interest.py`
script. 

As you can see, it's very close to a native function already.

```python
# file: examples/compound_interest/call_compound_interest.py
from time import sleep

from lmrtfy import catalog  #1

job = catalog.calc_compound_interest(5., 10., 5) #2

if job:
    print(job.id, job.status)
    
    while not job.ready: #3
        sleep(1.)
    
    print(job.results) #4
```

Run the script with your local python interpreter `python examples/compound_interest/call_compound_interest.py`
to make use of the deployed script.

The output of the script looks like this:
```shell
INFO Validating auth token.
INFO Auth token accepted.
INFO Valid access token found. Login not necessary.
INFO Updated function catalog.
INFO Added function calc_compound_interest.
INFO Job 78b69e45-3d51-4734-92db-a4901ee6d02b created. Status is RUNNING.
78b69e45-3d51-4734-92db-a4901ee6d02b JobStatus.RUNNING
{'compound_interest': 2.7628156250000035}
```

The ID of the job is going to be different from the one shown in the example output.

Let's discuss some aspects of the code a little closer:

1. Importing the catalog triggers the catalog update to get newly deployed functions every time you
run the code
2. The function `calc_compount_interest` is now part of the catalog and can be called just like a 
normal function in your code, however this function is not executed locally and run wherever the 
corresponding runner is deployed.
3. Loop until the job is ready. In this context `ready` means that the results are ready to be fetched.
which can simply be done by calling `job.results`. The return value is a dictionary with the keys
corresponding to the names of the results and the values are the actual values of the result.

## Using the CLI

LMRTFY also provides a way to submit jobs with the `lmrtfy` CLI tool. All you need for this
is a `profile_id` which is provided by you during the deployment and a JSON file that contains the input
parameters.

!!! attention
    This is a good way to call deployed scripts from another language as you can always build the
    JSON file and call the `lmrtfy` CLI. **If you are using it this we, please contact us. We want to
    provide more native-feeling interfaces to languages other than python as well but would love to 
    hear what you use to priortize.**

For the example calculating the compound interest, the JSON file would look like this:
```json
{
  "argument_values": {
    "annual_interest": 6.0,
    "principal": 5000.0,
    "years": 10
  },
  "argument_units": {
    "annual_interest": "%"
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
