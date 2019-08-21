#!/bin/env/python
# -*- encoding: utf-8 -*-
"""

"""
from __future__ import print_function, division
import time
import ray

import pype


@ray.remote
def f(server):
    while True:
        pype.pull_wait(server, 'data')
        data = ray.get(server.pull.remote('data'))

def main():
    ray.init()
    server = pype.Server.remote()
    server.add.remote('data', use_locking=True)

    f.remote(server)

    for i in range(20):
        pype.push_wait(server, 'data')
        server.push.remote(i, 'data')
        server.print_queue.remote('data')

    time.sleep(3)
    ray.shutdown()


if __name__ == "__main__":
    main()

