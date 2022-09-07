#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import numpy as np


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class Context(object):

    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass


def check_uuid4(test_str: str):
    """
    Checks whether job_od is a valid uuid4 or not.

    returns None if not, otherwise returns re.Match object
    """
    pattern = re.compile("[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
    return pattern.match(test_str)

