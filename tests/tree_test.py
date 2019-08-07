#!/bin/env/python
# -*- encoding: utf-8 -*-
"""

"""
from __future__ import print_function, division
import time
import ray

import pype


@ray.remote
def start(server, output_name):
    for i in range(100):
        while True:
            if ray.get(server.can_push.remote(output_name)):
                server.push.remote(i, output_name)
                break
            else:
                time.sleep(1e-4)


@ray.remote
def f(server, input_name, even_output_name, odd_output_name):
    while True:
        if ray.get(server.can_pull.remote(input_name)):
            data = ray.get(server.pull.remote(input_name))
            if data % 2 == 0:
                server.push.remote(data, even_output_name)
            else:
                server.push.remote(data, odd_output_name)
        else:
            time.sleep(1e-4)


def main():
    ray.init()
    server = pype.Server.remote()
    server.add.remote('data_0', use_locking=True)
    server.add.remote('data_1', use_locking=True)
    server.add.remote('data_2', use_locking=True)
    server.add.remote('data_3', use_locking=True)
    server.add.remote('data_4', use_locking=True)
    server.add.remote('data_5', use_locking=True)
    server.add.remote('data_6', use_locking=True)

    start.remote(server, 'data_0')

    f.remote(server, 'data_1', 'data_2')
    f.remote(server, 'data_2', 'data_3')
    f.remote(server, 'data_3', 'data_4')
    f.remote(server, 'data_4', 'data_5')
    f.remote(server, 'data_5', 'data_6')

    for i in range(100):
        pype.pull_wait(server, 'data_6')
        data = ray.get(server.pull.remote('data_6'))
        print("Received ", data)
        server.print_queue.remote('data_6')

    time.sleep(3)
    ray.shutdown()

if __name__ == "__main__":
    main()