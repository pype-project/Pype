#!/bin/env/python
#-*- encoding: utf-8 -*-
"""

"""
from __future__ import print_function, division
import time
import ray


@ray.remote
class TestObject(object):

    def __init__(self, index):
        self.index = index

    def pull(self):
        return self.index


@ray.remote
class MainObject(object):

    def __init__(self):
        self.objects = []
        for i in range(10):
            self.objects.append(TestObject.remote(i))
        #print(self.objects[0]._ray_actor_id)


    def pull(self, index):
        return self.objects[index]._ray_actor_id


def main():
    ray.init()
    main_object = MainObject.remote()
    output = ray.get(main_object.pull.remote(0))
    print(output)

if __name__ == "__main__":
    main()