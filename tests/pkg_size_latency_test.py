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
def start(server, output_name):
    n_data = 10000
    data = np.random.randint(0, 10, (n_data))
    for i in range(100):
        pype.push_wait(server, output_name)
        server.push.remote(data, output_name)


@ray.remote
def f(server, input_name, output_name):
    while True:
        pype.pull_wait(server, input_name)
        data = ray.get(server.pull.remote(input_name))[0]
        pype.push_wait(server, output_name)
        server.push.remote(data, output_name)


def main():
    # ray.init()
    pype.init_ray()
    server = pype.Server.remote()
    server.add.remote('data_0', use_locking=False)
    server.add.remote('data_1', use_locking=False)
    server.add.remote('data_2', use_locking=False)
    ray.get(server.all_initalized.remote())

    start.remote(server, 'data_0')

    start_time = time.time()
    f.remote(server, 'data_0', 'data_1')
    f.remote(server, 'data_1', 'data_2')

    for i in range(100):
        pype.pull_wait(server, 'data_2')
        data = ray.get(server.pull.remote('data_2'))
        # print(data)
    elapsed = time.time()-start_time
    print("Elapsed: {}".format(elapsed))

    time.sleep(3)
    ray.shutdown()

if __name__ == "__main__":
    # start_time = time.time()
    # n_data = 1000000
    # data = np.random.randint(0, 10, (n_data))
    # print(time.time()-start_time)
    main()
