# Deploy the function (local runner)
Now you can deploy the function and make it available via the LMRTFY API. This is simply done by running

```shell
$ lmrtfy deploy <path_to_script.py> --local
```

The `--local` flag means that the script will run locally on your computer and waits for jobs from
the outside. The LMRTFY API only allows job submissions that fit your deployed annotation profile.

In the future you will be able to deploy directly to the cloud. Then, you do not have to host the runner
yourself.

!!! warning
    Don't change the script after you have deployed it. The current advice would be to copy and
    rename the script before deployment. In later versions, this will be taken care of by the lmrtfy 
    tool.

## Example
Let's assume that you want to deploy the example script `free_fall_lmrtfy.py` provided in 
`examples/free_fall/free_fall_lmrtfy.py`. This is simple done by running

```shell
$ cd examples/free_fall
$ python free_fall_lmrtfy.py # (1)!
$ lmrtfy deploy free_fall_lmrtfy.py --local
```

1. This step is necessary to create the annotation profile, but testing your script locally is likely
part of your development process. Therefore, often this step is not needed.

Running `lmrtfy deploy ... --local` does two things:

1. Register the function with name `free_fall_lmrtfy` in your [LMRTFY catalog](../web_app/catalog.md). 
If the function already exists it will be replaced **if** the input and output signatures have not 
changed. Otherwise, the profile will be rejected. You can force the replacement with the 
`--force-replacement` flag.
2. Start a runner on your local system that takes the submitted jobs and executes them. When you stop
the runner you won't receive any results from calling the function.

When a job is submitted the types of the job's input parameters are checked by the LMRTFY API. 
Furthermore, they are also checked for their bounds and their units. This way, only jobs that can 
be run successfully with your script will get executed by it.

# Deploying to the cloud

LMRTFY is currently not able to deploy your scripts directly to the cloud; however, you can do this 
manually by using `lmrtfy` inside of a docker container. The docker container can be run on your laptop,
one of your own servers or in the cloud.

The current workaround would be to use `lmrtfy` on a server or inside a docker container which can
be hosted in the cloud.

Inside the docker container you run the same command as if you were to run locally.

Easy cloud deployment will be added in the future.


