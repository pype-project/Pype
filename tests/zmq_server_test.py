#!/bin/env/python
#-*- encoding: utf-8 -*-
"""

"""
from __future__ import print_function
from __future__ import division
import numpy as np
import argparse
import socket
import types
import time
import tqdm
import sys
import os
import re

import config

# TCP_IP = '127.0.0.1'
# TCP_PORT = 5005
# BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((TCP_IP, TCP_PORT))
# s.listen(1)

# conn, addr = s.accept()
# print('Connection address:', addr)
# while 1:
#     data = conn.recv(BUFFER_SIZE)
#     if not data:
#       break
#     print("Client => Server Data: {}".format(data))
#     #print("received data:", data)
#     conn.send(b'Thanks client')  # echo

# conn.close()

# TCP_IP = '127.0.0.1'
# TCP_PORT = 5005
# BUFFER_SIZE = 1024
# MESSAGE = "Hello, World!"

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((TCP_IP, TCP_PORT))

# while True:
#   #time.sleep(1)
#   MESSAGE = "{}".format(time.time())
#   s.sendall(MESSAGE.encode())
#   data = s.recv(BUFFER_SIZE)
#   print("Server => Client Data: {}".format(data))
# s.close()

# print("received data:", data

import numpy as np
import base64
import zlib
import cv2
import sys
import zmq

"""
===============================================================================

===============================================================================
"""

def handle(data):
    return handle

class CameraInterface():

    def __init__(self):
        self.address = 'tcp://localhost:5555'

    def init_camera(self):
        context = zmq.Context()
        self.footage_socket = context.socket(zmq.PUB)
        self.footage_socket.connect(self.address)
        self.video_data = cv2.VideoCapture(0)  # init the camera

    def start_stream(self):
        context = zmq.Context()
        self.footage_socket = context.socket(zmq.PUB)
        self.footage_socket.connect(self.address)
        self.video_data = cv2.VideoCapture(0)  # init the camera
        while True:
            try:
                grabbed, frame = self.video_data.read()  # grab the current frame
                #frame = cv2.resize(frame, (640, 480))  # resize the frame
                #frame = cv2.resize(frame, (320, 240))  # resize the frame
                encoded, buffer = cv2.imencode('.jpg', frame)
                jpg_as_text = base64.b64encode(buffer)

                print(len(jpg_as_text))
                #jpg_as_text = zlib.compress(jpg_as_text)
                print(type(jpg_as_text))
                self.footage_socket.send(jpg_as_text)
            except KeyboardInterrupt:
                self.video_data.release()
                cv2.destroyAllWindows()
                break

    def fetch_frame(self,handle):
        context = zmq.Context()
        footage_socket = context.socket(zmq.SUB)
        footage_socket.bind('tcp://*:5555')
        footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

        while True:
            try:
                frame = footage_socket.recv_string()
                frame = frame.encode()
                #frame = zlib.decompress(frame)
                print(len(frame))
                print(type(frame))

                img = base64.b64decode(frame)

                npimg = np.fromstring(img, dtype=np.uint8)
                source = cv2.imdecode(npimg, 1)

                handle(source)

            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                break

def __main():
    ci = CameraInterface()

    if sys.argv[1] == 's':
        ci.start_stream()

    else:
        ci.fetch_frame(handle)


"""
===============================================================================

===============================================================================
"""


class DistAESServer():

    def __init__(self,
            server_addr=config.DEFAULT_SERVER_ADDR,
            server_port=config.DEFAULT_SERVER_PORT,
            n_workers=config.DEFAULT_NUM_WORKERS,
            worker_ips=None):
        self.server_addr = server_addr
        self.server_port = server_port
        self.n_workers = n_workers
        self.worker_ips = worker_ips

    #--------------------------------------------------------------------------

    def init_socket(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.s.connect((self.server_addr,self.server_port))

    #--------------------------------------------------------------------------

    def listen(self):
        while True:
            MESSAGE = "{}".format(time.time())
            s.sendall(MESSAGE.encode())
            data = s.recv(BUFFER_SIZE)
            print("Server => Client Data: {}".format(data))
        s.close()

"""
===============================================================================

===============================================================================
"""

def fetch_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server',required=True,type=str,
        default='{}:{}'.format(config.DEFAULT_SERVER_ADDR,
            config.DEFAULT_SERVER_PORT))

    args = parser.parse_args()
    print(args.server)

    assert isinstance(args.server,str),('Invalid arg type: {}'.format(
        type(args.server).__name__))

    re_check = re.search("((\d{1,3}.){3}\d:\d{1,5})", args.server)
    if re_check == None:
        raise UserWarning("Invalid server arg: {}".format(args.server))

    assert re_check.group() == args.server,("Invalid server arg: {}".format(
        args.server))

    return args.server

#------------------------------------------------------------------------------

"""
===============================================================================

===============================================================================
"""

def main():
    (server_host,server_port) = fetch_args()
    server = DistAESServer(server_addr=server_addr,server_port=server_port)

if __name__ == "__main__":
    main()


