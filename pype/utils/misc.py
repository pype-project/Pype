#!/bin/env/python
# -*- encoding: utf-8 -*-
"""

"""
from __future__ import print_function, division
import time
import ray

from pype.utils.exceptions import QueueTimeoutError


def pull_wait(server,
              queue: str,
              wait_time: float = 5e-3,
              batch_size: int = None,
              timeout: int = 300):
    """

    :param server:
    :param queue:
    :param wait_time:
    :param batch_size:
    :param timeout:
    :return:
    """
    start_time = time.time()
    while True:
        if ray.get(server.can_pull.remote(
                queue, batch_size=batch_size)):
            break
        else:
            if time.time() - start_time > timeout:
                raise QueueTimeoutError(
                    "Timeout for {}", format(queue))
            time.sleep(wait_time)


def push_wait(server,
              queue: str,
              wait_time: float =5e-3,
              timeout: int = 300):
    """

    :param server:
    :param queue:
    :param wait_time:
    :param timeout:
    :return:
    """
    start_time = time.time()
    while True:
        if ray.get(server.can_push.remote(queue)):
            break
        else:
            if time.time()-start_time > timeout:
                raise QueueTimeoutError(
                    "Timeout for {}",format(queue))
            time.sleep(wait_time)