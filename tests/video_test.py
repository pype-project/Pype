#!/bin/env/python
# -*- encoding: utf-8 -*-
"""

"""
from __future__ import print_function, division
import cv2
import ray

import pype


def main():
    ray.init()
    server = pype.Server.remote()
    video_server = pype.VideoServer.remote(server, camera=0, output_queues=('frames'))

    while True:
        data = ray.get(server.pull.remote('frames'))
        if len(data) > 0:
            frame = data['frame']
            cv2.imshow('frames', frame)
            cv2.waitKey(1)


if __name__ == '__main__':
    main()
