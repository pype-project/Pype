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
    pype.init_ray()
    server = pype.Server.remote()
    server.add.remote('frames', use_locking=False, batch_lock=10)
    video_server = pype.VideoServer.remote(server, camera=0, scale=0.5,
                                           output_queues=('frames'))
    while True:
        pype.pull_wait(server, 'frames', batch_size=10)
        data = ray.get(server.pull.remote('frames', batch_size=10,
                                          wrap=False, flip=True))
        if len(data) > 0:
            print("Len batch: ", len(data))
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