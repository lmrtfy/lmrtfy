This is our quick start guide. Everything you need to know to get started is here.

# Installation
You can install the [lmrtfy package](https://pypi.org/project/lmrtfy/) just like any other package:

```shell
$ pip install lmrtfy
```

If you use conda you need to install `pip` in your conda environment before you can use LMRTFY. This
is likely necessary on Windows.

```shell
$ conda install pip
$ pip install lmrtfy
```

# Sign-Up
To make full use of LMRTFY you need to sign up with us with `lmrtfy login`.

Besides an e-mail-based sign up we also provide social logins via GitHub and Google for ease of use.

# Calling your first remote function
Calling a function that is available in the cloud is as easy as calling a native function.

```py title="call_example1.py" linenums="1" 
from time import sleep
from lmrtfy.functions import catalog 

job = catalog.examples.example1(args) # (1)!
 
while job and not job.ready: # (2)!
    sleep(1.)

if job:    
    print(job.results)  # (3)!


```

1. This calls the function `example1` in the LMRTFY namespace `example`. The function is executed
   on a remote resource.
2. If `job` is not valid the call did not succeed. `job.ready` queries the job status and becomes
   true once the results are ready.
3. `job.results` gets the results from LMRTFY as JSON:
```json
{
  "<variable name>": <value>,
  ...
}    
```

As you can see calling the function `example1` looks just like calling any other function in Python;
however, it is actually eexcuted on a remote server, in this case on our own server as we provide the
example.

Each call to a deployed function returns a `Job` object if the submission was successful. If an error
occurred `None` is returned. This way we can check if the submission was successful or not.

To get the results from the computation we can simply call `job.results`. Depending on the size of the
results this call will take a while. In the example, this call should at most take a few seconds.

# Deploy your first function
Deploying your own function is really easy, too.

Let's say you want to calculate how fast a falling object will be after $x$ seconds:

The code which can be used with LMRTFY is really simple:

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

The highlighted lines have been added or changed to let LMRTFY know about the structure of the script.

Before we can deploy the function we need to run it through the Python interpreter once to create
the annotation profile.

```shell
$ python free_fall_lmrtfy.py 
```

To deploy this function on your laptop you simply run
```shell
$ lmrtfy deploy free_fall_lmrtfy.py --local
```
This makes the function available in your catalog as `free_fall_lmrtfy` and starts a runner on your
laptop. Nobody but you can call the function unless you share it with others. When you stop the
runner calling this function will not yield any results.

Calling the deployed function becomes as simple as `#!python catalog.free_fall_lmrtfy(time=200.)`.
