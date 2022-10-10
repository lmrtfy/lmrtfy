#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from lmrtfy.functions import catalog

job = catalog.free_fall_lmrtfy(time=100.0)

if job:
    while not job.ready:
        time.sleep(1)

    print(job.results)