#!/bin/env/python
# -*- encoding: utf-8 -*-
"""

"""
import base64
import sys
import time

import cv2
import numpy as np
import zmq


def handle(data):
    cv2.imshow('data', data)
    cv2.waitKey(1)
    return handle


class CameraInterface():

    def __init__(self):
        self.address = 'tcp://localhost:5555'

    def init_camera(self):
        context = zmq.Context()
        self.footage_socket = context.socket(zmq.PUB)
        self.footage_socket.connect(self.address)
        self.video_data = cv2.VideoCapture(0)

    def start_stream(self):
        context = zmq.Context()
        self.footage_socket = context.socket(zmq.PUB)
        self.footage_socket.connect(self.address)
        self.video_data = cv2.VideoCapture(0)

        while True:
            try:
                grabbed, frame = self.video_data.read()
                encoded, buffer = cv2.imencode('.jpg', frame)
                jpg_as_text = base64.b64encode(buffer)
                self.footage_socket.send(jpg_as_text)

            except KeyboardInterrupt:
                self.video_data.release()
                cv2.destroyAllWindows()
                break

    def fetch_frame(self, handle):
        context = zmq.Context()
        footage_socket = context.socket(zmq.SUB)
        footage_socket.bind('tcp://*:5555')
        footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

        start_time = time.time()
        for i in range(1000):

            try:
                frame = footage_socket.recv_string()
                frame = frame.encode()

                img = base64.b64decode(frame)

                npimg = np.fromstring(img, dtype=np.uint8)
                source = cv2.imdecode(npimg, 1)

                # handle(source)

            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                break

        elapsed = time.time() - start_time
        print(1000 / elapsed)


def main():
    """Test ZMQ FPS Test"""
    ci = CameraInterface()

    if sys.argv[1] == 's':
        ci.start_stream()
    elif sys.argv[1] == 'c':
        ci.fetch_frame(handle)
    else:
        raise UserWarning("Use s (server) or c (client) arg")


if __name__ == "__main__":
    main()
