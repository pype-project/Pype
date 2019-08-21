#!/bin/env/python
# -*- encoding: utf-8 -*-
"""

"""
from __future__ import division, print_function

import ray

from pype.servers.queue import RayQueue
from pype.utils.exceptions import QueueExistsError, QueueNotFoundError


@ray.remote
class Server(object):

    def __init__(self,
                 verbose: bool = True,
                 queue_type='FIFO'):
        self.queue_type = queue_type
        self.queues = {}
        self.verbose = verbose

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
        self.add(queue)

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

    def _verify_queue_arg(self, queues: str):
        """

        :param queues:
        :return:
        """
        if not isinstance(queues, (str, list, tuple)):
            raise TypeError(
                "Queue must be type (str, list, tuple), not {}".format(
                    type(queues).__name__))

    def all_initalized(self):
        for q in self.queues.keys():
            active = ray.get(self.queues[q].is_active.remote())
            print("Queue {} is initialized.".format(q))

    def queue_len(self, queue):
        return ray.get(self.queues[queue].queue_len.remote())

    def len(self) -> int:
        """

        :return:
        """
        return len(self.queues)

    def print_queue(self,
                    queue: (str, list, tuple),
                    verify: bool = False):
        """

        :param queue:
        :param verify:
        :return:
        """
        if verify:
            self._verify_queue_arg(queue)
        self.queues[queue].print_queue.remote()

    def add(self,
            queue: str,
            use_locking: bool = False,
            use_semaphore: bool = False,
            semaphore: int = 10,
            batch_lock: int = None,
            max_data_len: int = -1
            ):
        """

        :param queue:
        :param use_locking:
        :param use_semaphore:
        :param semaphore:
        :param max_data_len:
        :return:
        """
        if not isinstance(queue, str):
            raise TypeError("Queue must be type str, not {}".format(
                type(queue).__name__))
        if not (queue in self.queues.keys()):
            if self.verbose:
                print("Creating new queue: {}".format(queue))
            self.queues[queue] = RayQueue.remote(
                use_locking=use_locking,
                use_semaphore=use_semaphore,
                semaphore=semaphore,
                batch_lock=batch_lock)
        else:
            # TODO: Fix QueueExistsError input
            raise QueueExistsError("{} already exists".format(queue))

    def pull(self,
             queue: (str, list, tuple),
             batch_size: int = 1,
             index: int = -1,
             wrap: bool = False,
             remove: bool = True,
             create: bool = True,
             flip: bool = False,
             verify: bool = False) -> list:
        """

        :param queue:
        :param create:
        :return:
        """
        if verify:
            self._verify_queue_arg(queue)
        if not (queue in self.queues.keys()):
            if create:
                self.__add__(queue)
            return []
        else:
            if ray.get(self.queues[queue].can_pull.remote()):
                return ray.get(self.queues[queue].pull.remote(
                    index=index,
                    batch_size=batch_size,
                    wrap=wrap,
                    remove=remove,
                    verify=verify,
                    flip=flip))
            else:
                return []

    def push(self,
             data,
             queues: (str, list, tuple),
             create: bool = True,
             verify: bool = True,
             expand: bool = False) -> None:
        """
        Push data to the selected queue(s)
        :param data:
        :param queues:
        :param create:
        :param verify:
        :param expand:
        :return:
        """
        # Wrap the queues for queue iteration
        if isinstance(queues, str):
            queues = [queues]

        # Verify that the user args are correct
        if verify:
            # Check queues arg type
            self._verify_queue_arg(queues)

            # Check for multiple instances of queue names
            queue_names = list(self.queues.keys())
            for q in queues:
                if queue_names.count(q) > 1:
                    raise Exception("Multiple queue counts of {}".format(q))

        # Iterate over the target queues and push the data
        for q in queues:
            # If the queue is not created yet, create or exit
            if not (q in self.queues.keys()):
                if create:
                    self.__add__(q)
                else:
                    # TODO: Fix QueueNotFoundError input
                    raise QueueNotFoundError('{} not found'.format(q))

            # Push data to target queue
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
                 batch_size=None,
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
        return ray.get(self.queues[queue].can_pull.remote(
            batch_size=batch_size))
