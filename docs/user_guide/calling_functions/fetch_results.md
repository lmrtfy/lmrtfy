# Fetching results in your code
When you call a function from your code, the results are part of the job object created when [calling
the function](submission.md).

You can only get the results when they are ready by using `job.results`:

```python
while not job.ready:
    sleep(1.)

print(job.results)
```

Currently, the while loop is necessary to wait for the results. This isn't the most ergonomic way
to do this. 

This could easily become a future (in the sense of concurrent programming) later on. **We are also 
looking for feedback, what would work best for you.**

# Get results with the CLI
LMRTFY also provides a way to download the results of the computation. All you need is the `<job_id>`
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