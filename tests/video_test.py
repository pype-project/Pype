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
    server.add.remote('frames', use_locking=False)
    video_server = pype.VideoServer.remote(server, camera=0, scale=1, output_queues=('frames'))
    while True:
        data = ray.get(server.pull.remote('frames', batch_size=-1, flip=True))
        # print(data)
        if len(data) > 0:
            print(ray.get(server.queue_len.remote('frames')))
            print("len data ", len(data))
            for d in data:
                frame = d['frame']
                cv2.imshow('frames', frame)
                cv2.waitKey(1)
        else:
            time.sleep(1e-4)


if __name__ == '__main__':
    main()

