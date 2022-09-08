

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





