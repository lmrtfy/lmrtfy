
The `lmrtfy` CLI tools uses the following schema:

```shell
lmrtfy [COMMAND] [COMMAND_OPTIONS]
```

where `[COMMAND]` is one of the following: `login`, `logouot`, `deploy`, `submit`, and `fetch`.

# Commands
## `login`
The usage of the LMRTFY services is connected to a user accouunt. With `lmrtfy login` you can directly
trigger the login process. This is usually not necessary, because each command that needs a valid
authorization token will trigger the login if needed.

## `logout`
Logout of the currently active account. This should only be necessary in special cases, e.g. if you
have more than one account for some reason (private and work account for example).

## `deploy <scipt> [OPTIONS]` 
This command deploys the `<script>` and makes it available via the LMRTFY platform. It's now ready 
to take jobs.

!!! note 
    Currently, only local deployment via the `--local` flag works. If you want to deploy to the cloud
    you need to manually do this and run `lmrtfy deploy <script> --local` on the remote resource.


| Option | Description                                                  |
|--------|--------------------------------------------------------------|
| `--local` | Deploy locally on the current system.                     |
| `--run_as_daemon` | Run the deployment as daemon in the background.   |


## `submit <profile_id> <arguments.json>`

The CLI allows you to submit jobs for a specific `profile_id` which is returned by the `deploy` step.

`<argument.json>` needs to contain valid input data, otherwise the job is rejected. The structure
of the JSON file can be found [here](user_guide/calling_functions/submission.md#using-the-cli).

## `fetch <job_id> <path>`

It's also possible to fetch the results from a job with `job_id`. The job ID is displayed during the 
submission step. 

With `<path>` you specify where the results should be saved.