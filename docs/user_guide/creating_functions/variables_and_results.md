The API reference with the corresponding function signatures for `variable` and `result` can be 
found [here](../../api_reference/annotation.md).

In this part we want to take a closer look at some details.

# Transparency

The annotation functions `variable` and `result` are transparent for the Python interpreter.

Let's say we have the following code:
```python linenums="1"
x = variable(5., name="x")

tmp = heavy_computation(x)

y = result(tmp, name="y")
```

To the Python interpreter the code looks more or less like this:
```python linenums="1"
x = 5

tmp = heavy_computation(x)

y = tmp
```

The calls to `variable` and `result` always return the value itself. In the background, these calls
create the annotation which is necessary for the LMRTFY platform. 

When a function is deployed the `variable` functions injects the input arguments of the
job received through the LMRTFY platform into the script. The `result` function on the other hand 
funnels the result back to the LMRTFY platform which makes it available to the caller of the function.


# Validity check

If you checked the [API reference](../../api_reference/annotation.md) you may have noticed that
`variable` and `result` have some additional parameters: `min`, `max`, and `unit`. Even better, 
through the first argument, the actual value, you also create type information that allows us to 
thoroughly check incoming job submissions.

## Type check

The input type is inferred from the value that is used in the `variable` function call.

| function call                                     | inferred type of `x` | accepted type with LMRTFY          |
|---------------------------------------------------|----------------------|------------------------------------|
| `#!py x = variable(5, name="x")`                  | `#!py int`           | `#!py int`                         |
| `#!py x = variable(5., name="x")`                 | `#!py float`         | `#!py float`                       |
| `#!py x = variable([5, 2], name="x")`             | `#!py int_array`     | `#!py list[int], ndarray[int] `    |
| `#!py x = variable([5.,2.], name="x")`            | `#!py float_array`   | `#!py list[float], ndarray[float]` |
| `#!py x = variable("abc", name="x")`              | `#!py str`           | `#!py str`                         |
| `#!py x = variable(["abc", "def"], name="x")`     | `#!py str_array`     | `#!py list[str]`                   |
| `#!py x = variable(["abd", 1, 1.1], name="x")`    | `#!py json`          | `#!py list[any]`                   |
| `#!py x = variable({"a": "a", "b": 1}, name="x")` | `#!py json`          | `#!py dict`                        |

If the input arguments submitted via the catalog do not match the accepted type, we reject the job
and tell the caller to fix their types. We chose a strict type checking because a type has its meaning
which it might lose during automatic conversion.

## Bounds check

The `min` and `max` parameters limit the range in which numeric input variables are seen as valid.
This is especially useful if your algorithm has known and well-defined limitations. If it only works
between $0$ and $1000$ you can simply specify `#!py variable(500, name="a", min=0, max=1000)`.

When a job is submitted via the LMRTFY platform, these bounds are checked. If the input variable `a`
is out of bounds we notify the caller and reject the job.

## Unit check

Another useful thing is the annotation with an actual `unit` for the variable. Currently, this is
done via `str` but we will switch to [pint units](https://pypi.org/project/Pint/) in later releases.

Similar to the numeric bounds the units are checked during the job submission and the job is rejected
if the unit do not match.

!!! example
    In 1999 the [NASA](https://www.nasa.gov) lost its Mars Climate Orbiter due to a navigation error,
    which was caused by a [failure to convert units from the imperial system to the metric system](https://solarsystem.nasa.gov/missions/mars-climate-orbiter/in-depth/).
