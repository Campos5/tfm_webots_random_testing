from __future__ import absolute_import

import argparse
import jinja2
import json
import random
import os
import subprocess
import tempfile
import time

from io import StringIO
from hypothesis import given, settings, assume, HealthCheck, target
from hypothesis.strategies import integers, floats, lists
from time import sleep

import config_test
from world_core import config
from world_core.random_world import World

NUM_EXAMPLE = 0
start_time = None
num_objects = None


@given(
    x=floats(0.0, 1.0), 
    y=floats(0.0, 1.0), 
    #n=integers(1, 10), 
    #m=integers(1, 10), 
    num_object=integers(0, config.NUM_OBJECTS)
)
@settings(max_examples=5)#, suppress_health_check=(HealthCheck.too_slow,))
def adding_one_element(x, y, num_object):
    
    x = int(x * 10)
    y = int(y * 10)
    
    print(x,y)
    
    """
    Test using random parameters.
    In this case 
    """
    object_to_add = list(config.POSSIBLE_OBJECTS.keys())[num_object]
    print(object_to_add)
    world = World(10, 10, config.TEMPLATE_PATH)
    print(world.room)
    assume(world.check_space(object_to_add, x, y, 0))

    # Necessary because template range map is from -5 to 5
    # And world.room is from 0 to 10
    x = x - 5
    y = y - 5
    
    print('object added in', x, y)
    world.add_element_with_translation(object_to_add, x, y)
    world.jinja_template.stream(elements=world.objects).dump(config.TEST_MAP_PATH)

    command = 'webots {}'.format(config.TEST_MAP_PATH)
    webots_process = subprocess.Popen(
        command.split(), 
        stdout=subprocess.PIPE, 
        shell=True
    )

    TIMEOUT = 20    
    while TIMEOUT > 0:
        stdout = webots_process.communicate()[0]
        print(stdout)
        TIMEOUT -= 1
        time.sleep(1)

    print('TIMEOUT')
    webots_process.terminate()
    webots_process.wait()


@given(
    positions=lists(lists(integers(0, 9), min_size=2, max_size=2), min_size=1, max_size=config.WORLD_MAX_OBJECTS),
    objects_to_add=lists(integers(0, config.NUM_OBJECTS - 1), min_size=1, max_size=config.WORLD_MAX_OBJECTS)
)
@settings(max_examples=5, suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,))
def adding_multiples_elements(positions, objects_to_add):
    assume(len(positions) == len(objects_to_add))

    world = World(10, 10, config.TEMPLATE_PATH)
    for i, (x, y) in enumerate(positions):
        object_to_add = list(config.POSSIBLE_OBJECTS.keys())[objects_to_add[i]]
        assume(world.check_space(object_to_add, x, y, 0))
        # Necessary because template range map is from -5 to 5
        # And world.room is from 0 to 10
        x = x - 5
        y = y - 5
        world.add_element_with_translation(object_to_add, x, y)

    #world.jinja_template.stream(elements=world.objects).dump(config.TEST_MAP_PATH)
    """
    command = 'webots - {}'.format(config.TEST_MAP_PATH)
    webots_process = subprocess.Popen(
        command.split(), 
        stdout=subprocess.PIPE,
        stdin=StringIO(world.jinja_template.render(elements=world.objects)).getvalue().encode(),
        shell=True
    )"""

    from subprocess import run, PIPE

    p = run(
        ['webots'], 
        stdout=PIPE,
        input=world.jinja_template.render(elements=world.objects), 
        encoding='ascii',
        shell=True
    )


@given(
    x=integers(0, 10), 
    y=integers(0, 10),
    num_object=integers(0, config.NUM_OBJECTS)
)
@settings(max_examples=5)#, suppress_health_check=(HealthCheck.too_slow,))
def adding_one_target_element(x, y, num_object):
    global NUM_EXAMPLE
    
    target(1.0)    
    object_to_add = list(config.POSSIBLE_OBJECTS.keys())[num_object]
    world = World(10, 10, config.TEMPLATE_PATH)
    assume(world.check_space(object_to_add, x, y, 0))
    world.add_element_with_translation(object_to_add, x, y)
    
    map_file = config.TEST_MAP_PATH.replace('.wbt', '{}.wbt'.format(NUM_EXAMPLE))
    world.jinja_template.stream(elements=world.objects).dump(map_file)
    NUM_EXAMPLE += 1
    
    
    command = 'webots {}'.format(map_file)
    webots_process = subprocess.Popen(
        command.split(), 
        stdout=subprocess.PIPE, 
        shell=True
    )

    TIMEOUT = 20
    sleep(TIMEOUT)
    
    webots_process.terminate()
    webots_process.wait()
    os.remove(map_file)

@given(
    positions=lists(lists(integers(0, 99), min_size=2, max_size=2), min_size=config_test.NUM_OBJECTS, max_size=config_test.NUM_OBJECTS),
    objects_to_add=lists(integers(0, config.NUM_OBJECTS - 1), min_size=config_test.NUM_OBJECTS, max_size=config_test.NUM_OBJECTS)
)
@settings(max_examples=5, suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,))
def adding_multiples_target_elements(positions, objects_to_add):    
    global NUM_EXAMPLE
    global start_time
    
    if not start_time:
        start_time = time.time()

    world = World(10, 10, config.TEMPLATE_PATH)
    last_x, last_y = 0, 0
    for i, (x, y) in enumerate(positions):
        # Trying to maximize distance between two objects
        target(float(x - last_x))
        target(float(y - last_y))
        
        object_to_add = list(config.POSSIBLE_OBJECTS.keys())[objects_to_add[i]]
        assume(world.check_space(object_to_add, x, y, 0))
        world.add_element_with_translation(object_to_add, x, y)
        last_x, last_y = x, y

    map_file = config.TEST_MAP_PATH.replace('.wbt', '{}.wbt'.format(NUM_EXAMPLE))
    world.jinja_template.stream(elements=world.objects).dump(map_file)
    NUM_EXAMPLE += 1

    print('Execution time with {} objects:'.format(len(positions)), time.time() - start_time)
    start_time = None

    command = 'webots {}'.format(map_file)
    webots_process = subprocess.Popen(
        command.split(), 
        stdout=subprocess.PIPE, 
        shell=True
    )

    # De momento se ejecuta webots eternamente. Se detiene cerrando la ventana de webots.
    """
    TIMEOUT = 300
    sleep(TIMEOUT)
    
    webots_process.terminate()
    webots_process.wait()
    """
    #os.remove(map_file)


if __name__ == "__main__":
    adding_multiples_target_elements()