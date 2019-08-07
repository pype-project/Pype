#!/bin/env/python
# -*- encoding: utf-8 -*-
"""

"""
from __future__ import print_function, division
import time
import ray
import sys
import os


def init_ray(remove_existing=True, temp_dir=None):
    if remove_existing:
        if ray.is_initialized():
            ray.shutdown()
    if temp_dir is None:
        dir_name = os.path.dirname(os.path.abspath(__file__))
        temp_dir = os.path.join(dir_name, 'ray_temp_dir_{}'.format(
            '_'.join(str(time.time()).split('.'))))
    object_store_memory = int(
        0.6 * ray.utils.get_system_memory() // 10 ** 9 * 10 ** 9)
    ray.init(
        include_webui=False,
        ignore_reinit_error=True,
        # plasma_directory=temp_dir,
        # temp_dir=temp_dir,
        object_store_memory=object_store_memory,
    )
    #ray.init(temp_dir=temp_dir)