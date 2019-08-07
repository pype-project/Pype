#!/bin/env/python
# -*- encoding: utf-8 -*-
"""

"""
from __future__ import print_function, division
import time
import ray

import pype
from pype.utils.ray_functions import init_ray


@ray.remote
def f(server):
    for i in range(20):
        server.push.remote(i, 'data')
        print("pushed ", i)
        time.sleep(1)


def main():
    init_ray()
    server = pype.Server.remote()
    server.add.remote('data', use_locking=False)
    f.remote(server)

    for i in range(4):
        pype.pull_wait(server, 'data', batch_size=5)
        data = ray.get(server.pull.remote('data', batch_size=5, wait_batch=True))
        print(data)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ray.shutdown()
