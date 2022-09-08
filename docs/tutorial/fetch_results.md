# Get results
lmrtfy also provides a way to download the results of the computation. All you need is the `<job_id>`
that you received when you submitted the job. Then, you simply run

```shell
$ lmrtfy fetch <job_id> <save_path>
```

The results will be saved in `<save_path>/<job_id>/..`.  Each result is currently saved as a JSON
file with the following format:

```js
{
    "<var_name>": <value>
}
```

Each variable has its own file. 

!!! warning
    This will very likely change in the future to be more ergonomic.