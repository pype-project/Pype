#!/bin/env/python
# -*- encoding: utf-8 -*-
"""

"""
from __future__ import print_function, division
import numpy as np
import time
import ray

import pype


@ray.remote
def f(data):
    output = data
    return 1


def main():
    pype.init_ray()
    ray.get(f.remote(1))
    time.sleep(10)
    for i in range(1000):
        data = np.random.randint(0,10,(i*10, i*10))
        start_time = time.time()
        ray.get(f.remote(data))
        elapsed = time.time() - start_time
        print(elapsed)


if __name__ == "__main__":
    main()