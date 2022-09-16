#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep

from lmrtfy import catalog

job = catalog.calc_compound_interest(5., 10., 5)

if job:
    print(job.id, job.status)
    while not job.ready:
        sleep(1.)

    print(job.results)