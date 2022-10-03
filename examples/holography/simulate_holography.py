import numpy as np
import scipy as sp

from lmrtfy.annotation import variable, result

#input definitions
cell = variable(5, name="cell")  # variable
size = variable(1023, name="size")  # variable

b = np.zeros((size, size))
x = np.linspace(-5., 5., size)
X, Y = np.meshgrid(x, x)
k = np.cos(30 * (np.sqrt(X ** 2 + Y ** 2))) * np.exp(-(X ** 2 + Y ** 2) / 1.)
i = np.zeros((size, size))

cx = np.asarray(np.round(np.random.rand(cell) * (size - 1)), dtype=int)
cy = np.asarray(np.round(np.random.rand(cell) * (size - 1)), dtype=int)

for m in range(cell):
    i[cx[m], cy[m]] = 1.

h = sp.signal.fftconvolve(i, k)[int(size / 2):-int(size / 2),
    int(size / 2):-int(size / 2)]  # result

h = result(h, name="h")
