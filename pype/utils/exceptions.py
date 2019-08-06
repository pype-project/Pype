#!/bin/env/python
# -*- encoding: utf-8 -*-
"""

"""
from __future__ import print_function, division


class QueueNotFoundError(Exception):

    def __init__(self, message, errors):
        super().__init__(self, message, errors)
        self.errors = errors


class QueueExistsError(Exception):

    def __init__(self, message, errors):
        super().__init__(self, message, errors)
        self.errors = errors