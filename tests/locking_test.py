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
        if ray.get(server.can_pull.remote('data')):
            data = ray.get(server.pull.remote('data'))
        else:
            time.sleep(1e-2)


def main():
    ray.init()
    server = pype.Server.remote()
    server.add.remote('data', use_locking=True)

    f.remote(server)

    for i in range(20):
        pype.push_wait('data')
        server.push.remote(i, 'data')
        server.print_queue.remote('data')

    time.sleep(3)
    ray.shutdown()


if __name__ == "__main__":
    main()

