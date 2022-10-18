---
hide:
    - tags
tags:
    - Introduction
---

**Let Me Run That For You.**

✅ Create functions that run in the **cloud**, on **your servers** or even on **your laptop**.

✅ Call them from code that runs somewhere else, just **like a regular function**.

✅ **Share functions** with friends and colleagues, track their usage and **monetize** their usage.

✅ Works with Python, but more languages will be added in the future.

<div style="text-align: center;" markdown>

[![Web App](https://img.shields.io/badge/LMRTFY-WebApp-blue?style=for-the-badge)](https://app.lmrt.fyi)<br>
[![Website](https://img.shields.io/badge/website-lmrt.fyi-blue?style=for-the-badge)](https://lmrt.fyi)<br>
[![GitHub Repository](https://img.shields.io/badge/repository-GitHub-blue?style=for-the-badge)](https://github.com/lmrtfy/lmrtfy)
[![Badge_BSD3](https://img.shields.io/badge/license-BSD--3-green?style=for-the-badge)](https://github.com/lmrtfy/lmrtfy/blob/main/LICENSE)
![Badge_Stars](https://img.shields.io/github/stars/lmrtfy/lmrtfy?style=for-the-badge)

</div>

* [Quickstart Guide](quickstart.md)
* [Tutorial](user_guide/installation.md)
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

!!! info
    LMRTFY is currently in an early phase. Things will likely change in future releases.


## Quickstart - TL;DR
1. install with `pip install lmrtfy`
2. login/sign up with `lmrtfy login`
3. run `$ ipython` and `#!py from lmrtfy.functions import catalog`
4. call the provided example with `#!py job = catalog.examples.free_fall_lmrtfy(100.)`
5. get the results with `#!py job.results`

As you can see in step 4, it's as simple as calling a regular function from any other library
you have installed locally. 

## Examples
The [examples](examples/starting_example.md) are provided in the `examples/` directory. They are **work in progress**. As lmrtfy
matures, more and more examples will be added.

If you miss an example for a specific use case, please let us know, and we will add one!
