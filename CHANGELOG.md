# v0.0.6 - 08/sep/2022
* changed input formats for json as follow:S
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

to
```json
{
  "argument_values": {
    "time": 6.0
  },
  "argument_units" : {
    "time": "s"
  }
}
```
* modified readme to match docs
* added check if job_id is valid UUID



# v0.0.5 - 06/sep/2022
* included version check 
* changed listener to remove profile collisions

# v0.0.4 - 05/sep/2022
* First release

This creates the following commands:
* `lmrtfy login` => get token
* `lmrtfy deploy <script.py> --local`=> get profile_id for deployed script profile
* `lmrtfy submit <profile_id> <input.json>` => get job_id for submitted job
* `lmrtfy fetch <job_id> <path_to_save>` => get results for finished job