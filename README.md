# lmrtfy

![Linter](https://github.com/lmrtfy/lmrtfy/workflows/linter.yml/badge.svg) [![Documentation Status](https://readthedocs.org/projects/lmrtfy/badge/?version=latest)](https://lmrtfy.readthedocs.io/en/latest/?badge=latest)

Turn variables into program arguments. Auto-generates a CLI interface and an API using lmrt.fyi.

# Installation
Installation is really easy via pip:
```shell
$ pip install lmrtfy
```

# Usage
Using lmrtfy is straight-forward. In contrast to many other tools the goal is to have only minimal
changes in your code. Currently, you only need to annotate the input variables and the results variables.

From the annotations a profile is automatically generated that contains the relevant information.

```python
import numpy as np
from lmrtfy.annotation import variable, result  # (1)


x = variable(5, name="x", min=1, max=10) (2)
y = variable(np.linspace(0., 1., 101, dtype=np.float64), name="y", min=-1., max=11., unit="m") (3)
z = variable("abc", name="z")

z1 = variable(["abc", "def"], name="z1")
z2 = variable(["abc", 1, 1.1], name="z2")
z3 = variable({'a': "abc", 'b': 1}, name="z3")

a = result(x * y, name="a") (4)
b = result(x * z, name="b")
```

* (1) import `variable` and `result` function to annotate your code
* (2) `x` is a variable with the default value `5` which can take values between `1` and `10`.
* (3) `y` is a variable of type numpy.ndarray which holds 101 values between `0.` and `1.` The valid
range is between `-1` and `11´ and the unit of this variable is meter.
* (4) `a` is a result which is computed by `x * y`.

## Run the script locally

This is really easy. We do not change your development process and you run your script exactly as usual:
```shell
$ python your_script.py
```

During this step, we also create the annotation profile which will later be used to deploy the functionality.

## Share your app with others

Currently, you can share your script's functionality by running
```shell
$ lmrtfy deploy local <your_script.py>
```

This command will create an API endpoint which can be used to send jobs to your script. The script will stay
on your computer and will only accept jobs that have inputs matching the description in your `variable` statements
in the code. The inputs will be checked for their type, their valid range, their unit and their name. This
way only valid jobs will even reach your code.


# License
![BSD 3-Clause License](https://github.com/lmrtfy/lmrtfy/blob/main/LICENSE)
