#!/bin/env/python
# -*- encoding: utf-8 -*-
"""

"""
from __future__ import print_function, division
import ray

from pype.servers.fifo_server import RayFIFOQueue
from pype.utils.exceptions import QueueNotFoundError, QueueExistsError


@ray.remote
class Server(object):

    def __init__(self,
                 verbose: bool=True):
        self.queues = {}
        self.verbose = verbose

    def len(self) -> int:
        """

        :return:
        """
        return len(self.queues)

    def __len__(self) -> int:
        """

        :return:
        """
        return len(self.queues)

    def __add__(self,
                queue: str):
        """

        :param queue:
        :return:
        """
        if not isinstance(queue, str):
            raise TypeError("Queue must be type str, not {}".format(
                type(queue).__name__))
        if not (queue in self.queues.keys()):
            if self.verbose:
                print("Creating new queue: {}".format(queue))
            self.queues[queue] = RayFIFOQueue.remote()
        else:
            # TODO: Fix QueueExistsError input
            raise QueueExistsError("{} already exists".format(queue))

    def add(self,
            queue: str):
        """

        :param queue:
        :return:
        """
        self.__add__(queue)

    def __sub__(self,
                queue: str):
        """

        :param queue:
        :return:
        """
        if not isinstance(queue, str):
            raise TypeError("Queue must be type str, not {}".format(
                type(queue).__name__))
        if queue in self.queues.keys():
            # TODO: Delete remote process
            pass

    def pull(self,
             queue: (str, list, tuple),
             create: bool = True) -> list:
        """

        :param queue:
        :param create:
        :return:
        """
        if not isinstance(queue, (str, list, tuple)):
            raise TypeError(
                "Queue must be type (str, list, tuple), not {}".format(
                    type(queue).__name__))
        if not (queue in self.queues.keys()):
            if create:
                self.__add__(queue)
            return []
        else:
            if ray.get(self.queues[queue].can_pull.remote()):
                return ray.get(self.queues[queue].pull.remote())
            else:
                return []

    def push(self,
             data,
             queues: (str, list, tuple),
             create: bool = True,
             verify: bool = True,
             expand: bool = False) -> None:
        """
        
        :param data:
        :param queues:
        :param create:
        :param verify:
        :param expand:
        :return:
        """
        if isinstance(queues, str):
            queues = [queues]
        if verify:
            if not isinstance(queues, (str, list, tuple)):
                raise TypeError(
                    "Queues must be type (str, list, tuple) not {}".format(
                        type(queues).__name__))
            queue_names = list(self.queues.keys())
            for q in queues:
                if queue_names.count(q) > 1:
                    raise Exception("Multiple queue counts of {}".format(q))
        for q in queues:
            if not (q in self.queues.keys()):
                if create:
                    self.__add__(q)
                else:
                    # TODO: Fix QueueNotFoundError input
                    raise QueueNotFoundError('{} not found'.format(q))
            self.queues[q].push.remote(data, expand=expand)

    def can_push(self,
                 queue,
                 create=True):
        """

        :param queue:
        :param create:
        :return:
        """
        if not (queue in self.queues.keys()):
            if create:
                self.__add__(queue)
            else:
                return False
        return ray.get(self.queues[queue].can_push.remote())

    def can_pull(self,
                 queue,
                 create=False):
        """

        :param queue:
        :param create:
        :return:
        """
        if not isinstance(queue, str):
            raise TypeError("Queue must be type str, not {}".format(
                type(queue).__name__))
        if not (queue in self.queues.keys()):
            if create:
                self.__add__(queue)
            else:
                return False
        return ray.get(self.queues[queue].can_pull.remote())
