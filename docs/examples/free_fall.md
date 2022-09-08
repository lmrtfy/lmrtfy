# Example 2: Velocity due to gravtity in free fall
The second example calculates the velocity of an object falling from the sky (without air resistance).

The standard gravity on earth is 9.81 m*s^(-2). Multiplicated by the fall time, we will get the velocity
of the object after that time.

If you like equations more, you might recognize these from your physics class:
$$
v = g \cdot t
$$

In regular python code that you run locally it would look like this:
```python
standard_gravity = 9.81
time = 200.

velocity = standard_gravity * time
print(f"Velocity after {time} seconds is {velocity} m/s.")
```

Now we want to be able to share that functionality via the lmrtfy web API. All we have to do is decide
which variables are considered to be an input and a result of the computation:

```python
from lmrtfy import variable, result

standard_gravity = 9.81
time = variable(200., name="time", min=0, max=1000, unit="s")

velocity = result(standard_gravity*time, name="velocity", min=0, max=9810, unit="m/s")
print(f"Velocity after {time} seconds is {velocity} m/s.")
```

Now run `$ python examples/velocity_from_gravity/calc_velocity.py` to generate the required profile.
This way you can also check if your code is actually working the way you expect it.

To deploy, you simply run `$ lmrtfy deploy examples/velocity_from_gravity/calc_velocity.py --local`.
Do not stop that process, because than you will not be able to submit a job.

Open a new terminal in the same directory and run `$ lmrtfy submit <profile_id>`. The profile_id has been
printed in the `lmrtfy deploy` step. This does not work right out of the box, because you need to
specify a JSON file that contains the input parameters for your job. A template for that JSON should
have been printed in the CLI.

Create such a JSON file and name it `input.json` and put values of the correct type into the values (no type conversion is
happening in the API, so if `float` is required, you cannot input an `int`).

Now run `$ lmrtfy submit <profile_id> input.json`. You will receive a `job_id` which we will shortly
need to fetch the results after they are computed.

After your job has run, you can get the results by running `$ lmrtfy fetch <job_id> <path to store results>`.
The results are downloaded and stored inside the specified path within a directory that has the
`job_id` as its name.
