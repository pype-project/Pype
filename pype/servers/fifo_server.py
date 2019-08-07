#!/bin/env/python
# -*- encoding: utf-8 -*-
"""

"""
from __future__ import division, print_function

import time

import ray


class FIFOQueue(object):

    def __init__(self,
                 use_locking: bool = False,
                 use_semaphore: bool = True,
                 semaphore: int = 10,
                 start_at_right: bool = True,
                 max_data_len: int = -1):
        """

        :param use_locking:
        :param use_semaphore:
        :param semaphore:
        :param start_at_right:
        :param max_data_len:
        """
        if not isinstance(use_locking, bool):
            raise TypeError("use_locking arg must be boolean, not {}".format(
                type(use_locking).__name__))
        if not isinstance(use_semaphore, bool):
            raise TypeError("use_semaphore arg must be boolean, not {}".format(
                type(use_semaphore).__name__))
        if not isinstance(use_semaphore, int):
            raise TypeError("semaphore arg must be int, not {}".format(
                type(semaphore).__name__))
        if semaphore < 1:
            raise UserWarning("Semaphore must be > 0, not {}".format(
                semaphore))
        if use_semaphore and use_locking:
            raise UserWarning("Cannot have use_locking and use_semaphore")

        self._queue = []
        self.use_locking = use_locking
        self.use_semaphore = use_semaphore
        self.semaphore = semaphore
        # TODO: Implement max data len
        self.max_data_len = max_data_len
        # TODO: Better variable name
        self.start_at_right = start_at_right
        if use_locking:
            self.push_locked = False

    def print_queue(self):
        """

        :return: None
        """
        print(self._queue)

    def queue_len(self) -> int:
        """

        :return:
        """
        return len(self._queue)

    @staticmethod
    def preprocess_val(val):
        """

        :param val:
        :return:
        """
        return val

    @staticmethod
    def postprocess_val(val):
        """

        :param val:
        :return:
        """
        return val

    def can_pull(self, batch_size: int = None) -> bool:
        """

        :param batch_size:
        :return:
        """
        if not (batch_size is None):
            return len(self._queue) >= batch_size
        return len(self._queue) > 0

    def can_push(self) -> bool:
        """

        :param self:
        :return:
        """
        if self.use_locking:
            return not self.push_locked
        elif self.use_semaphore:
            return self.semaphore > 0
        else:
            return True

    def push(self, data, index=0, expand=False, verify=False) -> None:
        """

        :param data:
        :param index:
        :param expand:
        :param verify:
        :return: None
        """
        if self.use_locking:
            self.push_locked = True
        if expand:
            if verify:
                if not isinstance(data, list):
                    raise TypeError(
                        "Input data should be type list with expand=True")
            data = list(map(self.preprocess_val, data))
            if self.start_at_right:
                self._queue = self._queue[:index] + data + self._queue[index:]
            else:
                self._queue = (self._queue[:index + len(
                    self._queue)] + data + self._queue[index + 1:])
        else:
            data = self.preprocess_val(data)
            self._queue.insert(index, data)

    def pull(self,
             remove: bool = True,
             batch_size: int = 1,
             wait_batch: bool = False,
             wait_batch_time: float = 1e-4,
             index: int = -1,
             wrap: bool = False,
             verify: bool = True,
             flip: bool = True):
        """

        :param remove:
        :param batch_size:
        :param wait_batch:
        :param wait_batch_time:
        :param index:
        :param wrap:
        :param verify:
        :return:
        """
        if verify:
            if not isinstance(batch_size, int):
                raise TypeError("batch_size arg should be int, not: {}".format(
                    type(batch_size).__name__))
            if (batch_size < -1) or (batch_size == 0):
                raise UserWarning(
                    "batch_size should be -1 or > 0, not {}".format(
                        batch_size))
            if not isinstance(index, int):
                raise TypeError("index arg should be int, not: {}".format(
                    type(index).__name__))
            if not isinstance(wrap, int):
                raise TypeError("wrap arg should be boolean, not: {}".format(
                    type(wrap).__name__))
        if self.use_locking:
            self.push_locked = False
        if self.use_semaphore:
            self.semaphore += 1
        if wait_batch:
            if batch_size != -1:
                while True:
                    if len(self._queue) >= batch_size:
                        break
                    else:
                        time.sleep(wait_batch_time)
        if batch_size == -1:
            output = self._queue
        else:
            if (index == -1) and (batch_size == 1):
                output = self._queue[index:]
            elif (index == -1) and (batch_size != 1):
                output = self._queue[-batch_size:]
            # TODO: Add indexing with batch size
            # TODO: Positive indexes
        if len(output) == 0:
            return []
        output = list(map(self.postprocess_val, output))
        if not wrap:
            if batch_size == 1:
                output = output[0]
        if remove is True:
            if batch_size == -1:
                self._queue = []
            else:
                if index == -1:
                    self._queue = self._queue[:-batch_size]
        if flip:
            output.reverse()
        return output


@ray.remote
class RayFIFOQueue(FIFOQueue):

    def __init__(self,
                 use_locking: bool = False,
                 use_semaphore: bool = False,
                 semaphore: int = 10):
        """

        :param use_locking:
        :param use_semaphore:
        :param semaphore:
        """
        super().__init__(use_locking=use_locking,
                         use_semaphore=use_semaphore,
                         semaphore=semaphore)
