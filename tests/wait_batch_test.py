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
    for i in range(20):
        server.push.remote(i, 'data')
        print("pushed ", i)
        time.sleep(1)


def main():
    ray.init()
    server = pype.Server.remote()
    server.add.remote('data', use_locking=False)
    f.remote(server)
    for i in range(4):
        while True:
            if ray.get(server.can_pull.remote('data', batch_size=5)):
                break
            else:
                time.sleep(1e-2)
        data = ray.get(server.pull.remote('data', batch_size=5, wait_batch=True))
        print(data)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ray.shutdown()
