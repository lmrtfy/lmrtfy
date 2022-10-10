# Example 1: Simple annotation
This is a simple example to showcase the general usage of lmrtfy. It can be found 
in `examples/starting_example/example1.py`.

The two core concepts are the `variable` and `result` functions which annotate the inputs and
outputs of the script. They are needed to create the profile which is used to create the API.

```python title="example1.py" linenums="1"
import numpy as np
from lmrtfy.annotation import variable, result # (1)!


x = variable(5, name="x", min=1, max=10) # (2)!
y = variable(np.linspace(0., 1., 101, dtype=np.float64), name="y", 
             min=-1., max=11., unit="m") # (3)!
z = variable("abc", name="z")

z1 = variable(["abc", "def"], name="z1")  # (4)!
z2 = variable(["abc", 1, 1.1], name="z2") 
z3 = variable({'a': "abc", 'b': 1}, name="z3") 

a = result(x * y, name="a") # (5)!
b = result(x * z, name="b")
```

1. The functions need to be imported from the lmrtfy library
2. The variable `x` has the local value `5` and can be between 1 and 10.
3. You can have numpy arrays as inputs
4. Lists and dictionaries work, too!
5. Results are similar to variables. They have a name and an expression that they will become.

Run `python examples/starting/example1.py` to create the profile needed for the deployment.

## Deployment
To deploy the script run `lmrtfy deploy examples/starting/example1.py --local`

## Call `example1` from code
Now you can simply call `catalog.example1()` with the correct arguments, and you are good to go:
```py title="call_example1.py" linenums="1"
import time

from lmrtfy.functions import catalog

job = catalog.<your_namespace>example1(x=1,   # (1)!
                       y=[1, 2.0, 3.0],
                       z="foobar",
                       z1=["bar", "foo"],
                       z2=["foo", 1, 42],
                       z3={"foo": "bar", "bar": "foo"}
                       )
                      
if job:
    while not job.ready:
        time.sleep(1)

    print(job.results)
```

1. `<your_namespace>` is your private namespace on LMRTFY, which is typically your nickname.
Available namespaces are shown when importing `catalog` or when calling `catalog.update()`. 

`if job:` is currently required to ensure that you actually got a job object back from the function 
which would not be the case if the submission failed.

## Calling `example1` from the CLI

!!! note
    We encourage you to use code to submit jobs and get results. 

During the deployment you should  have received a seven letter `profile_id`:
```shell
Profile_id to be used for requests: CgHUejl
```

We need the `profile_id` to submit a job from the CLI:

```shell
lmrtfy submit CgHUejL examples/starting/example1.json
```

If the JSON file has the correct inputs, in a valid range with correct units you will see that the
job submission was successful. You will receive a ten-letter job ID.

```shell
INFO Job submission successful.
INFO Job-id: HgaUbcTFah
```

With this `job_id` you can now get the job results:
```shell
lmrtfy fetch HgaUbcTFah .  
```

That's all that is to it. Happy Hacking!