#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pathlib import Path

import numpy as np


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


p = Path('dummy_data')
try:
    print('mk dummy_data dir:', p.mkdir())
except FileExistsError:
    print('dummy data dir already exists.')

data = {}
data['x'] = 3.
data['y'] = np.linspace(5.,6.,101)
data['z'] = "DEF"

data['z1'] = ["m", "n"]
data['z2'] = ["p", 3]
data['z3'] = {'g': "asd", 'v': 3.123}

for k in data:
    with p.joinpath(f'lmrtfy_variable_{k}.json').open(mode='w') as f:
        json.dump({k: data[k]}, f, cls=NumpyEncoder)
