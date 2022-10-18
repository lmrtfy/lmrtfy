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
To make full use of LMRTFY you need to [sign up](https://app.lmrt.fyi) with us with `lmrtfy login`.

_You can sign up with GitHub to streamline the process._

# Calling your first remote function
Calling a function that is available in the cloud is as easy as calling a native function.

```py title="IPython listing - Best way to call jobs interactively" linenums="1" 
$ ipython
In [1]: from lmrtfy.functions import catalog
# information regarding the configuration
2022-10-12 12:14:28 [36627] INFO {'namespaces': ['examples', 
'<user_namespace>' ]} # (1)!

In [2]: job = catalog.examples.free_fall_lmrtfy(time=100.) # (2)!
2022-10-12 12:16:08 [36627] INFO Job 8GXvA6JREr created. 
Status is ACCEPTED. # (3)!

In [3]: job.ready # (4)!
Out[3]: True

In [4]: job.results  # (5)!
Out[5]: {'velocity': 981.0}
```

1. If you want to know more about namespaces go [here](user_guide/namespaces.md).
2. This calls the function `free_fall_lmrtfy` in the LMRTFY namespace `example`. The function is executed
   on a remote resource that has been provided by us.
3. The job is created and that status is `ACCEPTED`. Sometimes the computation is so quick that it 
immediately returns `RESULTS_READY`.
4. `job.ready` checks if the results are computed and ready to be fetched with `job.results`
5. `job.results` gets the results from LMRTFY as JSON:
```json
{
  "<variable name>": <value>,
  ...
}    
```

As you can see calling the function `free_fall_lmrtfy` looks just like calling any other function in Python;
however, it is actually executed on a remote server, in this case on our own server as we provide the
example.

Each call to a deployed function returns a `Job` object if the submission was successful. If an error
occurred `None` is returned. This way we can check if the submission was successful or not. 

_If you get an error here, please let us know via [hello@lmrt.fyi](mailto:hello@lmrt.fyi) or open an 
[issue](https://github.com/lmrtfy/lmrtfy/issues)._

To get the results from the computation we can simply call `job.results`. Depending on the size of the
results this call will take a while. In the example, this call should at most take a few seconds.

# Deploying your first function
Deploying your own function is really easy, too.

Let's say you want to calculate how fast a falling object will be after $x$ seconds.

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
This makes the function available in your catalog as 
```catatlog.<user_namespace>.free_fall_lmrtfy```
and starts a runner on your laptop. 

Nobody but you can call the function unless you 
[share it](user_guide/sharing/sharing.md) with others. 

If no runner is deployed an error will be returned.

