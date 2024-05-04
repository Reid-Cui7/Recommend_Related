import numpy as np
import matplotlib.pyplot as plt


data = np.loadtxt(
    "/Users/mac/Codes/Data/temperature_icecream.csv",
    dtype=float,
    skiprows=1,
    usecols=(0,1),
    delimiter=",",
    encoding="utf8"
)

x = data[:, 0]
y = data[:, 1]

def func(p, x):
    k, b = p
    return k * x + b

def cost(p, x, y):
    k, b = p
    data_num = x.shape[0]
    loss = np.sum((func(p, x) - y) ** 2) / data_num
    return loss ** 0.5

def grad(initial_p, lr, max_item):
    k, b = initial_p
    cost_list = []
    for i in range(max_item):
        k, b = step_grad(k, b, lr, x, y)
        _cost = cost([k, b], x, y)
        cost_list.append(_cost)
    return k, b, cost_list


def step_grad(k, b, lr, x, y):
    k -= lr * np.sum((func([k, b], x) - y) * x) / x.shape[0]
    b -= lr * np.sum(func([k, b], x) - y) / x.shape[0]
    return k, b

initial_p = [0, 0]
lr = 0.0001
max_item = 30

k, b, cost_list = grad(initial_p, lr, max_item)
print(cost_list)
plt.plot(cost_list)
plt.show()