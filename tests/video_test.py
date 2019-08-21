#!/bin/env/python
# -*- encoding: utf-8 -*-
"""

"""
from __future__ import division, print_function

import time

import ray

import pype


def main():
    """Test Pype Video Streaming FPS"""
    ray.init()
    server = pype.Server.remote()
    server.add.remote('frames', use_locking=True)
    pype.VideoServer.remote(server, camera=0, scale=1, output_queues=('frames'))

    counter = 0
    start_time = time.time()

    while True:
        pype.pull_wait(server, 'frames')
        data = ray.get(
            server.pull.remote('frames', batch_size=-1, flip=True, wrap=True))
        counter += len(data)
        # for d in data:
        #     frame = d['frame']
        #     cv2.imshow('frames', frame)
        #     cv2.waitKey(1)
        if counter >= 1000:
            break

    elapsed = time.time() - start_time
    print('FPS: ', counter / elapsed)


if __name__ == '__main__':
    main()
