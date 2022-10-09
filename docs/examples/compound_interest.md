# Example 3: Compound interest

The third example calculates the compound interest $C$ starting from a principal value $P$ with
annualt interest $I$ after $N$ years:

$$
C = P \cdot (1 + I)^N - P
$$

Very common formula in anything related to finance.

Again, we start with the plain code, as you would implement it right away:
```py title="calc_compound_interest.py" linenums="1"
def compound_interest(principal: float, annual_interest: float, years: int):
    return principal * (1. + annual_interest/100.)**years - principal

principal = 10_000
interest = 6
years = 10
ci = compound_interest(principal, interest, years)
print(f"Compound interest after {years} years: {ci}")
```

You can run this example with `$ python ci.py` and it should print `7908.47`. Which is the compound
interest after 10 years if you started with 10000 units that grow by 6% each year.

There are several problems with this solution:
1. You need to change the code to run it for other inputs
2. Units are unclear! `principal` is a currency, but that actually does not matter. The real problem
   is the `interest`. Is it decimal or in %?

# Annotate with lmrtfy

Using lmrtfy, you would annotate the script as follows:
```py title="calc_compound_interest_lmrtfy.py" linenums="1" hl_lines="1 10-13 17"
from lmrtfy.annotation import variable, result

def compound_interest(principal: float, annual_interest: float, years: int):
   return principal * (1. + annual_interest/100.)**years - principal

principal = 10_000.
interest = 6.
years = 10

principal = variable(principal, name="principal", min=0)
annual_interest = variable(principal, name="annual_interest", 
                           min=0, max=100, unit="%")
years = variable(years, name="years", min=0)

ci = compound_interest(principal, annual_interest, years)

ci = result(ci, name="compound_interest")

```

Now, we run `python calc_compound_interest_lmrtfy_1.py` to generate the profile.

!!! warning
    The type annotation are not enforced when run locally. LMRTFY checks the types and units only
    if jobs are submitted through its API. This guarantees that you can run your code without our
    service.

# Deployment

After creating the profile we can easily deploy with
```shell
$ lmrtfy deploy examples/compound_interest/calc_compound_interest.py --local
```

## Call `compound_interest` from code
Similar to the other examples we just need to import the `catalog` and call the correct function:
```py title="call_compound_interest.py" linenums="1"
from time import sleep

from lmrtfy.functions import catalog

job = catalog.calc_compound_interest_lmrtfy(5., 10., 5)

if job:
   print(job.id, job.status)
   while not job.ready:
      sleep(1.)

   print(job.results)
```

## Call `compound_interest` from the CLI
The output should be similar to this:
```text
INFO Profile_id to be used for requests: <profile_id>
```

The `<profile_id>` is important to submit jobs. 


To submit a job you are currently required to save the input parameters as JSON (e.g. `input.json`):
```json title="input.json to calculate compound interest"
{
  "argument_values": {
    "annual_interest": 6.0,
    "principal": 5000.0,
    "years": 10
  },
  "argument_units": {
    "annual_interest": "%"
  }
}
```

Now, we have everything that is needed to start a job:
```shell
$ lmrtfy submit <profile_id> input.json
```

The job id for this job is printed to the terminal:
```text
INFO Job-id: <job_id>
```

We need the `<job_id>` later to fetch the results from the computation. 

# Alternative Annotation
A more compact but working alternative is to create the result as follows:
```python title="Alternative annotation" linenums="1"
from lmrtfy.annotation import variable, result

def compound_interest(principal: float, annual_interest: float, years: int):
    return principal * (1. + annual_interest/100.)**years - principal

if __name__ == "__main__":
    ci = result(
        compound_interest(
            principal=variable(10000., name="principal", min=0),
            annual_interest=variable(6, name="annual_interest", min=0, max=100, unit="%"),
            years=variable(10, name="years", min=0)
        ),
        name="compound_interest"
    )
    print(ci)
```

It's not necessarily prettier to look at, but also works!
