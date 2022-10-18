#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from lmrtfy.functions import catalog

job = catalog.examples.finding_pmf_lmrtfy()

if job:
    while not job.ready:
        time.sleep(1)

    print(job.results)
