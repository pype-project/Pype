#!/bin/env/python
#-*- encoding: utf-8 -*-
"""

"""
from __future__ import print_function, division
import numpy as np
import time
import gzip
import ray
import sys


@ray.remote
def bouncer(data):
    return data


def main():
    ray.init()
    size = 2000
    time_sum = 0
    n_iterations = 100
    data = np.random.uniform(-1, 1, (size, size))
    print(sys.getsizeof(data))
    data = gzip.compress(data, 9)
    print(sys.getsizeof(data))
    #gzip.compress()
    for i in range(n_iterations):
        start_time = time.time()
        ray.get(bouncer.remote(data))
        time_sum += time.time()-start_time
        print(time.time()-start_time)

    print(time_sum/n_iterations)

if __name__ == "__main__":
    main()



