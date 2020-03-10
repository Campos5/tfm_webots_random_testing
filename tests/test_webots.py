from __future__ import absolute_import

import argparse
import jinja2
import json
import random
import os
import subprocess
import time

from hypothesis import given, assume, HealthCheck
from hypothesis.strategies import integers, floats

from world_core import config
from world_core.random_world import World


@given(x=floats(0.1, 0.9), y=floats(0.1, 0.9), n=integers(1, 10), m=integers(1, 10))
def adding_one_element(x, y, n, m):
    
    x = n * x - n
    y = m * y - m
    
    """
    Test using random parameters.
    In this case 
    """
    objects = []

    print((x, y, n, m))
    world = World(n, m, config.TEMPLATE_PATH)

    world.add_element_with_translation(world.possible_objects, objects, x, y)
    world.jinja_template.stream(elements=world.objects).dump(config.TEST_MAP_PATH)

    command = 'webots {}'.format(config.TEST_MAP_PATH)
    print(command)
    webots_process = subprocess.Popen(command.split())
    
    time.sleep(10)
    print('TIMEOUT')
    webots_process.terminate()
    webots_process.wait()
    

@given(n=integers(1, 10), m=integers(1, 10), o=integers(1, 10))
def adding_n_elements(n, m, num_objects):
    objects = []
    
    world = World(n, m, config.TEMPLATE_PATH)
    
    for _ in num_objects:
        world.add_element(world.possible_objects, objects)
    
    world.jinja_template.stream(elements=world.objects).dump(config.TEST_MAP_PATH)

    command = 'webots {}'.format(config.TEST_MAP_PATH)
    webots_process = subprocess.Popen(command.split())

    '''
    time.sleep(10)
    print('TIMEOUT')
    webots_process.terminate()
    webots_process.wait()
    '''
    
if __name__ == "__main__":
    adding_one_element()