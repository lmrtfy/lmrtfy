#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from lmrtfy import catalog

job = catalog.calc_velocity(time=100.0)

if job:
    while not job.ready:
        time.sleep(1)

    print(job.results)