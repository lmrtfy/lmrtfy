#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lmrtfy import variable, result

"""
This script calculates the velocity of an object in free fall after `time` seconds.
"""

time = variable(200., name="time", min=0, max=1000, unit="s")
speed = result(9.81*time, name="speed", min=0, max=9810, unit="m/s")
