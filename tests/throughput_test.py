#!/bin/env/python
# -*- encoding: utf-8 -*-
"""

"""
from __future__ import print_function, division
import random
import time
import ray
import sys
import os

import pype


@ray.remote
class NullVideoServer(object):

    def __init__(self, server,
                 wait=True,
                 input_queue='frame',
                 output_queues='person'):
        self.server = server
        self.input_queue = input_queue
        self.wait = wait
        if isinstance(output_queues, str):
            self.output_queues = [output_queues]
        else:
            self.output_queues = output_queues
        self.main()

    def main(self):
        """

        :return:
        """
        while True:
            data = time.time()
            data = ray.put(data)
            if self.wait:
                pype.push_wait(self.server, self.output_queues[0])
            self.server.push.remote(data, self.output_queues)




@ray.remote
class NullDetector(object):

    def __init__(self, server,
                 input_queue='frame',
                 output_queues='person',
                 batch_size=-1):
        self.server = server
        self.input_queue = input_queue
        if isinstance(output_queues, str):
            output_queues = [output_queues]
        self.output_queues = output_queues
        self.batch_size = batch_size
        # self.model = None
        # self.model.warmup()
        self.main()

    def main(self):
        while True:
            pype.pull_wait(self.server,
                           self.input_queue,
                           batch_size=self.batch_size)
            data = ray.get(self.server.pull.remote(
                self.input_queue,
                batch_size=self.batch_size,
                wrap=True))
            # self.model.infer(data)
            for q in self.output_queues:
                self.server.push.remote(data, self.output_queues, expand=True)




def main():
    #pype.init_ray()
    ray.init()

    ray.timeline(filename="timeline.json")

    server = pype.Server.remote()
    server.add.remote('frame', use_locking=False)
    #server.add.remote('person', use_locking=False)
    # # server.add.remote('face', use_locking=False)
    server.add.remote('pose', use_locking=False)
    server.add.remote('object', use_locking=False)
    server.add.remote('action', use_locking=False)
    # server.add.remote('action', use_locking=False)
    # server.add.remote('action1', use_locking=False)
    # server.add.remote('counter', use_locking=False)
    # server.add.remote('results')


    person_models = [NullDetector.remote(server, input_queue='frame',
                                         output_queues=['pose'],
                                         batch_size=-1) for _ in range(1)]
    person_models = [NullDetector.remote(server, input_queue='pose',
                                         output_queues=['object'],
                                         batch_size=-1) for _ in range(1)]
    person_models = [NullDetector.remote(server, input_queue='object',
                                         output_queues=['action'],
                                         batch_size=-1) for _ in range(1)]
    # person_models = [NullDetector.remote(server, input_queue='action',
    #                                      output_queues=['action1'],
    #                                      batch_size=-1) for _ in range(1)]
    # person_models = [NullDetector.remote(server, input_queue='action1',
    #                                      output_queues=['action2'],
    #                                      batch_size=-1) for _ in range(1)]
    # person_models = [NullDetector.remote(server, input_queue='action2',
    #                                      output_queues=['action3'],
    #                                      batch_size=-1) for _ in range(1)]
    # person_models = [NullDetector.remote(server, input_queue='action3',
    #                                      output_queues=['action4'],
    #                                      batch_size=-1) for _ in range(1)]
    # person_models = [NullDetector.remote(server, input_queue='action4',
    #                                      output_queues=['action5'],
    #                                      batch_size=-1) for _ in range(1)]
    # person_models = [NullDetector.remote(server, input_queue='action5',
    #                                      output_queues=['action6'],
    #                                      batch_size=-1) for _ in range(1)]
    # person_models = [NullDetector.remote(server, input_queue='action6',
    #                                      output_queues=['action7'],
    #                                      batch_size=-1) for _ in range(1)]
    time.sleep(3)
    ray.timeline(filename="timeline.json")
    for _ in range(1):
        NullVideoServer.remote(server, output_queues='frame')
    # person_models = [NullDetector.remote(server, input_queue='action1',
    #                                      output_queues=['action2'],
    #                                      batch_size=-1) for _ in range(1)]
    # person_models = [NullDetector.remote(server, input_queue='action2',
    #                                      output_queues=['action3'],
    #                                      batch_size=-1) for _ in range(1)]
    # person_models = [NullDetector.remote(server, input_queue='action3',
    #                                      output_queues=['action4'],
    #                                      batch_size=-1) for _ in range(1)]
    # person_models = [NullDetector.remote(server, input_queue='action4',
    #                                      output_queues=['action5'],
    #                                      batch_size=-1) for _ in range(1)]
    # person_models = [NullDetector.remote(server, input_queue='action5',
    #                                      output_queues=['action6'],
    #                                      batch_size=-1) for _ in range(1)]
    # person_models = [NullDetector.remote(server, input_queue='action6',
    #                                      output_queues=['action7'],
    #                                      batch_size=-1) for _ in range(1)]
    # pose_models = [NullDetector.remote(server, input_queue='pose',
    #                                    output_queues=['object']) for _ in range(1)]
    # face_models = [NullDetector.remote(server, input_queue='face',
    #                                    output_queues=['results']) for _ in range(1)]
    # counter_models = [NullDetector.remote(server, input_queue='person',
    #                                       output_queues=['results']) for _ in range(1)]
    # object_models = [NullDetector.remote(server, input_queue='object',
    #                                      output_queues=['action']) for _ in range(1)]
    # action_models = [NullDetector.remote(server, input_queue='action',
    #                                      output_queues=['results']) for _ in range(1)]
    ray.get(server.all_initalized.remote())
    time_elapsed = 0
    count = 0
    start_time = time.time()
    ray.timeline(filename="timeline.json")
    while True:
        pype.pull_wait(server, 'action')
        data = ray.get(server.pull.remote('action'))
            #time_elapsed += time.time()-data[0]
        count += len(data)
            # print(count)
        if time.time()-start_time > 10:
            ray.timeline(filename="timeline.json")
            break

    print("Throughput: {}".format(count/(time.time()-start_time)))
    ray.shutdown()
        # print("Processed {} frames".format(len(data)))
        # for d in data:
        #     frame = d['frame']
        #     dets = d['dets']

if __name__ == "__main__":
    main()

"""
123.12156349316523
78.85535030409181
60.73117300593765
"""