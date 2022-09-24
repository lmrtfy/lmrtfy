#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from lmrtfy.annotation import variable, result


x = variable(5, name="x", min=1, max=10)
y = variable(np.linspace(0., 1., 101, dtype=np.float64), name="y", min=-1., max=11., unit="m")
z = variable("abc", name="z")

z1 = variable(["abc", "def"], name="z1")
z2 = variable(["abc", 1, 1.1], name="z2")
z3 = variable({'a': "abc", 'b': 1}, name="z3")

a = result(x * y, name="a")
b = result(x * z, name="b")
