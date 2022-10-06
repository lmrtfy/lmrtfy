Now, we have seen how we can call a deployed function from our code, but how do we deploy something
ourselves?

This requires two main steps:

1. You need to [annotate](#annotate-your-script) your script to let LMRTFY know about the input 
variables and the results of your script.
2. The actual [deployment](deployment.md) of your script

# Annotate your script

The annotation of your script tells the lmrtfy tool which python variables are considered inputs and
outputs, which is done via the `variable` and `results` functions.

This step is important, because lmrtfy traces the calls to `variable` and `result` to create a profile
for the code. This profile includes the inputs and outputs as well as the additional meta information
(`min`, `max`, `unit`, and possibly more in the future).

Let's assume that you have create a script to calculate the velocity of an object after a certain time:
```py title="free_fall.py" linenums="1"
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

```py title="free_fall_lmrtfy.py" linenums="1" hl_lines="1 3 9"
from lmrtfy.annotation import variable, result # (1)!

time = variable(200., name="time", min=0, max=1000, unit="s") # (2)!
standard_gravity = 9.81

velocity = standard_gravity*time
print(f"Velocity after {time} seconds is {velocity} m/s.") 

velocity = result(velocity , name="velocity", min=0, max=9810, unit="m") # (3)!
```

1. `variable` and `result` are the imports that are needed to annotate your code to make it work
   with LMRTFY.
2. `variable` annotates any inputs of your script.
3. `result` annotates a result of script. A script can have multiple results.

If you run `python free_fall_lmrtfy.py` you get the exact same result as before. During the run, 
`lmrtfy` created the profile for `free_fall_lmrtfy.py` which will be needed to deploy the function.


## Create the annotation profile
It is required to run your script at least once with the regular python interpreter to create the
annotation profile which will be used to generate the API.
```shell
$ python <script.py>
```

The profile is currently saved under `~/.lmrtfy/profiles`. The profile is necessary for the deployment,
and is human-readable; however, there should be no need to check the created profile unless for 
troubleshooting


