#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from lmrtfy.functions import catalog

job = catalog.example1(x=1,
                       y=[1.0, 2.0, 3.0],
                       z="foobar",
                       z1=["bar", "foo"],
                       z2=["foo", 1, 42],
                       z3={"foo": "bar", "bar": "foo"}
                       )
#help(catalog.example1)

if job:
    while not job.ready:
        time.sleep(1)

    print(job.results)
