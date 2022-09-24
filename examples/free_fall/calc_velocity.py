#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lmrtfy.annotation import variable, result

"""
This script calculates the velocity of an object in free fall after `time` seconds.
"""

standard_gravity = 9.81
time = variable(200., name="time", min=0, max=1000, unit="s")

velocity = result(standard_gravity*time, name="velocity", min=0, max=9810, unit="m/s")
