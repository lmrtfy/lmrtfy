# Example

The examples are provided in the `examples/` directory. They are **work in progress**. As lmrtfy 
matures, more and more examples will be added. 

If you miss an example for a specific use case, please let us know and we will add one!

## Example 1: Simple annotation
This is a simple example to showcase the general usage of lmrtfy. It can be found 
in `examples/example1/example1.py`.

The two core concepts are the `variable` and `result` functions which annotate the inputs and
outputs of the script. They are needed to create the profile which is used to create the API.

```python
import numpy as np
from lmrtfy import variable, result # 1


x = variable(5, name="x", min=1, max=10) # 2
y = variable(np.linspace(0., 1., 101, dtype=np.float64), name="y", min=-1., max=11., unit="m") # 3
z = variable("abc", name="z")

z1 = variable(["abc", "def"], name="z1")  # 4
z2 = variable(["abc", 1, 1.1], name="z2") 
z3 = variable({'a': "abc", 'b': 1}, name="z3") 

a = result(x * y, name="a") # 5
b = result(x * z, name="b")
```

1. The functions need to be imported from the lmrtfy library
2. The variable `x` has the local value `5` and can be between 1 and 10.
3. You can have numpy arrays as inputs
4. Lists and dictionaries work, too!
5. Results are similar to variables. They have a name and an expression that they will become.

## Example 2: Velocity due to gravtity in free fall
The second example calculates the velocity of an object falling from the sky (without air resistance).

The standard gravity on earth is 9.81 m*s^(-2). Multiplicated by the fall time, we will get the velocity
of the object after that time. 

In regular python code that you run locally it would look something like this:
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

## Example 3: Compound interest
TODO
```python
from lmrtfy import variable, result

def compound_interest(principal: float, annual_interest: float, years: int):
    return principal * (1. + annual_interest/100.)**years - principal

if __name__ == "__main__":
    ci = result(
        compound_interest(
            principal=variable(10000., name="principal", min=0),
            annual_interest=variable(0.06, name="annual_interest", min=0, max=100, unit="%"),
            years=variable(10, name="years", min=0)
        ),
        name="compound_interest"
    )
```

