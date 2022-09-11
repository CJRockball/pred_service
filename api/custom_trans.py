import numpy as np
""" This file contains transforms for the data pipeline """

def log_transform(x):
    return np.log(1+x)

def func(x):
    return np.log(x)

def inverse_func(x):
    return np.exp(x)