# Annotate your script

The annotation of your script tells the lmrtfy tool which python variables are considered inputs and
outputs, which is done via the `variable` and `results` functions.

This step is important, because lmrtfy traces the calls to `variable` and `result` to create a profile
for the code. This profile includes the inputs and outputs as well as the additional meta information
(`min`, `max`, `unit`, and possibly more in the future).

Let's assume that you have create a script to calculate the velocity of an object after a certain time:
```python
# file: free_fall.py
standard_gravity = 9.81
time = 200.

velocity = standard_gravity * time
print(f"Velocity after {time} seconds is {velocity} m/s.")
```

Now, if you want to recalculate for a different time, you would edit the script and run it again. While
this might work for a small script like this, this becomes tedious if you have different input variables
and want others to use your script easily, too.

Let's change the script in such a way that lmrtfy can create a profile which can be used to deploy
the function and make it available to other users:

```python
# file: free_fall_lmrtfy.py
# import the required things from lmrtfy
from lmrtfy import variable, result
standard_gravity = 9.81
# annotate an input
time = variable(200., name="time", min=0, max=1000, unit="s")

# annotate an output
velocity = result(9.81*time , name="velocity", min=0, max=9810, unit="m")
print(f"Velocity after {time} seconds is {velocity} m/s.")
```

If you run `python free_fall_lmrtfy.py` you get the exact same result as before. During the run, lmrtfy
created the profile for `free_fall_lmrtfy.py` which will be needed to deploy the function.


## Create the annotation profile
It is required to run your script at least once with the regular python interpreter to create the
annotation profile which will be used to generate the API.
```shell
$ python <script.py>
```

The profile is currently saved under `~/.lmrtfy/profiles` which will change in the future to respect
XDG directory specifications.

## Focus: `variable` and `result`

These functions are transparent. That means the assignment `a = variable(5, name="a")` assigns `a`
the value `5`. This way you can run the script simply with your local python interpreter if lmrtfy is
installed in the environment. `variable` and `result` do not have any external dependency (e.g. API calls)

The functions signatures are as follows. Only the first two arguments are required. Ideally, the
`name` argument should match the name of the variable you assign to, although that is not necessary.
It's considered to be a best practice, because it reduces possible errors and fosters a more intuitive
understanding of the code.
```python
# variable signature:
variable(value: supported_object_type, 
         name: str, 
         min = None, max = None, 
         unit: str = None) -> supported_object_type
# result signature:
result(value: supported_object_type,
        name: str,
        min = None, max = None,
        unit: str = None) -> supported_object_type
```

* The `value` argument specifies the default argument for the variable and has to be one of the
  supported types: `int, float, complex, bool, np.ndarray, list, dict`.
* `name` declares the name of the variable that will be used for the API generation. A sensible choice
  is the same name as the variable's name in the code itself.
* `min` and `max` can be used to specify boundaries for the input and output values in case they are
  numeric. This might come in handy if the code only works for certain input parameter ranges. If the
  inputs are outside the specified range the job will be rejected by the generated API.
* `unit` is a `str` that declares the unit of the variable/result. This is especially useful in scientific
  calculations where units are often not standardized and unclear.
