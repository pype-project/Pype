#!/bin/env/python
# -*- encoding: utf-8 -*-
"""

"""
from __future__ import print_function, division
import time
import cv2
import ray

import pype


def main():
    ray.init()
    server = pype.Server.remote()
    server.add.remote('frames', use_locking=False)
    video_server = pype.VideoServer.remote(server, camera=0, scale=1.,
                                           output_queues=('frames'))
    while True:
        data = ray.get(server.pull.remote('frames', batch_size=-1,
                                          wrap=True, flip=True))
        if len(data) > 0:
            for d in data:
                frame = d['frame']
                cv2.imshow('frames', frame)
                cv2.waitKey(1)
            print("Queue len: ", ray.get(
                server.queue_len.remote('frames')))
        else:
            time.sleep(1e-3)


if __name__ == '__main__':
    main()