
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


