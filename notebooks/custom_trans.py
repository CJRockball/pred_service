import numpy as np


def log_transform(x):
    return np.log(1+x)

def func(x):
    return np.log(x+1)

def inverse_func(x):
    return (np.exp(x) - 1)