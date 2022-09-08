# Submit a job
The lmrtfy tool also provides a way to submit jobs with the `lmrtfy` CLI tool. All you need for this
is a `profile_id` which is provided by you during the deployment and a JSON file that contains the input
parameters.

!!! info
    Later on, you will be able to see available `profile_id` on our web frontend

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
