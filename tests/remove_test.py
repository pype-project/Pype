#!/bin/env/python
# -*- encoding: utf-8 -*-
"""

"""
from __future__ import print_function, division
import time
import ray

import pype


def main():
    ray.init()

    data = list(range(100))

    server = pype.Server.remote()
    server.push.remote(data, 'data', expand=True)
    #server.print_queue.remote('data')
    #time.sleep(10)
    data = ray.get(server.pull.remote('data', batch_size=50, remove=False))
    print(data)
    ray.get(server.print_queue.remote('data'))


if __name__ == "__main__":
    main()
