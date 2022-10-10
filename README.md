<p align="center" width="66%">
   <a href="https://lmrt.fyi"><img alt="Logo" src="docs/images/lmrtfy_small.png" /></a>
</p>

<p align="center" width="100%">
   <a href="https://app.lmrt.fyi"></a><img alt="web app" src="https://img.shields.io/badge/LMRTFY-WebApp-blue?style=for-the-badge" /></a>
</p>

<p align="center" width="100%">
   <a href="https://lmrt.fyi"><img alt="Website badge" src="https://img.shields.io/badge/website-lmrt.fyi-blue?style=for-the-badge"/></a>
</p>

<p align="center">
   <a href="https://github.com/lmrtfy/lmrtfy"><img alt="repo badge" src="https://img.shields.io/badge/repository-GitHub-blue?style=for-the-badge" /></a>
   <img alt="GitHub Stars" src="https://img.shields.io/github/stars/lmrtfy/lmrtfy?style=for-the-badge" />
   <a href="https://github.com/lmrtfy/lmrtfy/blob/main/LICENSE"><img alt="BSD-3 badge" src="https://img.shields.io/badge/license-BSD--3-green?style=for-the-badge" /></a>
</p>

**LMRTFY stands for _Let Me Run That For You_.**

✅ Create functions that run in the **cloud**, on **your servers** or even on **your laptop**.

✅ Call them from code that runs somewhere else, just **like a regular function**.

✅ **Share functions** with friends and colleagues, track their usage and **monetize** their usage.

✅ Works with Python, but more languages will be added in the future.

---

![Linter](https://github.com/lmrtfy/lmrtfy/workflows/linter/badge.svg) 
[![Documentation (stable)](https://github.com/lmrtfy/lmrtfy/actions/workflows/publish_github_pages_stable.yml/badge.svg)](https://docs.lmrt.fyi/stable)
[![Documentation (latest)](https://github.com/lmrtfy/lmrtfy/actions/workflows/publish_github_pages_latest.yml/badge.svg)](https://docs.lmrt.fyi/latest)




* [Quickstart Guide](quickstart.md)
* [Tutorial](tutorial/installation.md)
* [Examples](examples/starting_example.md)
* [API Reference](api_reference/annotation.md)
* [How to report issues](report_bugs.md) and [how to contribute](contributing.md)

## Introduction

LMRTFY is a tool to share scripts via the cloud. Your scripts can run on your laptop, on your server
or in the cloud. You and everybody you shared your deployed script with can call the function straight
from their own code using the [lmrtfy package](https://pypi.org/project/lmrtfy/)

We strive to provide a frictionless developer experience:

* Change as little code as possible to use LMRTFY
* Call deployed function like any other function provided by a local library


## Quickstart - TL;DR
1. install with `pip install lmrtfy`
2. login/sign up with `lmrtfy login`
3. annotate your code's inputs with `variable` and its outputs with `result`
4. deploy the script:
    5.  `lmrtfy deploy examples/deployment/calc_compound_interest.py --local`
5. Use the deployed function (from another terminal, or another computer!):
    6. open `examples/calling_cloud_functions/call_function.py`
    7. run `python examples/call_deployed_function.py` to call the deployed function and get the results.

As you can see in step 5, it's as simple as calling a regular function from any other library
you have installed locally.

## Examples
The [examples](examples/starting_example.md) are provided in the `examples/` directory. They are **work in progress**. As lmrtfy
matures, more and more examples will be added.

If you miss an example for a specific use case, please let us know, and we will add one!

# License
![BSD 3-Clause License](https://github.com/lmrtfy/lmrtfy/blob/main/LICENSE)
