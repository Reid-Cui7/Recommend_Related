import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq


def func(p, x):
    a, b = p
    y = a * x + b
    return y

def errors(p, x, y):
    return y - func(p, x)


data = np.loadtxt(
    r"C:\Users\Bean1777\Documents\Codes\Daily\Data\temperature_icecream.csv",
    dtype=float,
    usecols=(0, 1),
    skiprows=1,
    encoding='utf8',
    delimiter=','
)

x = data[:, 0]
y = data[:, 1]

res = leastsq(errors, [1, 0], args=(x, y))
_a, _b = res[0]
print(res)

plt.scatter(x, y, color='red')
plt.plot(x, func([_a, _b], x), color='blue')
plt.show()