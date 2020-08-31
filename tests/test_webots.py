from __future__ import absolute_import

import argparse
import jinja2
import json
import random
import os
import subprocess
import time

from hypothesis import given, settings, assume, HealthCheck, target, Verbosity
from hypothesis.strategies import integers, floats, lists, composite

#from hamcrest import *

from datetime import timedelta
from time import sleep

import config_test
from world_core import config
from world_core.random_world import World

NUM_EXAMPLE = 0
start_time = None
num_objects = None


def distance_between_two_points(x, y):
    import math
    return math.sqrt((x[1] - x[0])**2 + (y[1] - y[0])**2)  


def get_num_of_sections(num_objects):
    import math
    x = math.sqrt(num_objects)
    return math.ceil(x)


@given(
    objects_to_add=lists(lists(integers(0, 99), min_size=3, max_size=3), min_size=config_test.MIN_NUM_OBJECTS, max_size=config_test.MAX_NUM_OBJECTS)
)
@settings(
    deadline=timedelta(milliseconds=10*1000), 
    max_examples=5, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    verbosity=Verbosity.verbose
)
def adding_multiples_elements(objects_to_add):    
    global NUM_EXAMPLE
    global start_time
    
    if not start_time:
        start_time = time.time()

    world = World(10, 10, config.TEMPLATE_PATH)

    for i, x, y in objects_to_add:
        num_possible_objects = len(list(config.POSSIBLE_OBJECTS.keys()))
        object_to_add = list(config.POSSIBLE_OBJECTS.keys())[i % num_possible_objects]
        assume(world.check_space(object_to_add, x, y, 0))
        world.add_element_with_translation(object_to_add, x, y)

    map_file = config.TEST_MAP_PATH.replace('.wbt', '{}.wbt'.format(NUM_EXAMPLE))
    world.jinja_template.stream(elements=world.objects).dump(map_file)
    NUM_EXAMPLE += 1

    print('Execution time with {} objects:'.format(len(objects_to_add)), time.time() - start_time)
    start_time = None

    command = 'webots {}'.format(map_file)
    webots_process = subprocess.Popen(
        command.split(), 
        stdout=subprocess.PIPE, 
        shell=True
    )

    # De momento se ejecuta webots eternamente. Se detiene cerrando la ventana de webots.
    """
    webots_process.terminate()
    webots_process.wait()
    """
    #os.remove(map_file)



@given(
    objects_to_add=lists(lists(integers(0, 99), min_size=3, max_size=3), min_size=config_test.MIN_NUM_OBJECTS, max_size=config_test.MAX_NUM_OBJECTS)
)
@settings(
    deadline=timedelta(milliseconds=10*1000), 
    max_examples=5, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    verbosity=Verbosity.verbose
)
def adding_multiples_elements_target_1(objects_to_add):    
    global NUM_EXAMPLE
    global start_time
    
    if not start_time:
        start_time = time.time()

    world = World(10, 10, config.TEMPLATE_PATH)
    #Target maximizing the number of objects to add 
    target(float(len(objects_to_add)), label="length")
    
    
    # Target maximizing distance between one point and the previous one
    distances = [0.0]
    last_x, last_y = 0, 0
    for i, x, y in objects_to_add:
        if i != 0:
            distances.append(distance_between_two_points((x, y), (last_x, last_y)))
        
        last_x, last_y = x, y
    
    target(float(sum(distances)), label="sum")

    for i, x, y in objects_to_add:
        num_possible_objects = len(list(config.POSSIBLE_OBJECTS.keys()))
        object_to_add = list(config.POSSIBLE_OBJECTS.keys())[i % num_possible_objects]
        assume(world.check_space(object_to_add, x, y, 0))
        world.add_element_with_translation(object_to_add, x, y)

    map_file = config.TEST_MAP_PATH.replace('.wbt', '{}.wbt'.format(NUM_EXAMPLE))
    world.jinja_template.stream(elements=world.objects).dump(map_file)
    NUM_EXAMPLE += 1

    print('Execution time with {} objects:'.format(len(objects_to_add)), time.time() - start_time)
    start_time = None

    command = 'webots {}'.format(map_file)
    webots_process = subprocess.Popen(
        command.split(), 
        stdout=subprocess.PIPE, 
        shell=True
    )

    # De momento se ejecuta webots eternamente. Se detiene cerrando la ventana de webots.
    """
    
    webots_process.terminate()
    webots_process.wait()
    """
    #os.remove(map_file)



@given(
    objects_to_add=lists(lists(integers(0, 99), min_size=3, max_size=3), min_size=config_test.MIN_NUM_OBJECTS, max_size=config_test.MAX_NUM_OBJECTS)
)
@settings(
    deadline=timedelta(milliseconds=10*1000), 
    max_examples=1, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    verbosity=Verbosity.verbose
)
def adding_multiples_elements_target_2(objects_to_add):    
    global NUM_EXAMPLE
    global start_time
    
    if not start_time:
        start_time = time.time()

    world = World(10, 10, config.TEMPLATE_PATH)
    
    #Target maximizing the number of objects to add 
    target(float(len(objects_to_add)), label="length")
    
    # Target maximizing distance between all point
    total_distance = 0.0
    for i, x1, y1 in objects_to_add:
        for j, x2, y2 in objects_to_add:
                total_distance +=distance_between_two_points((x1, y1), (x2, y2))
                
    target(float(total_distance), label="total_distance")

    for i, x, y in objects_to_add:
        num_possible_objects = len(list(config.POSSIBLE_OBJECTS.keys()))
        object_to_add = list(config.POSSIBLE_OBJECTS.keys())[i % num_possible_objects]
        assume(world.check_space(object_to_add, x, y, 0))
        world.add_element_with_translation(object_to_add, x, y)

    map_file = config.TEST_MAP_PATH.replace('.wbt', '{}.wbt'.format(NUM_EXAMPLE))
    world.jinja_template.stream(elements=world.objects).dump(map_file)
    NUM_EXAMPLE += 1

    print('Execution time with {} objects:'.format(len(objects_to_add)), time.time() - start_time)
    start_time = None

    command = 'webots --mode=fast --stdout --stderr {}'.format(map_file)
    webots_process = subprocess.Popen(
        command.split(), 
        stdout=subprocess.PIPE, 
        shell=True
    )

    execution_time = time.time()
    output = ''
    result = False
    while True:
        output = webots_process.stdout.readline().decode().strip()
        if output == '' and webots_process.poll() is not None: #or execution_time > config_test.TIMEOUT:
            break
        if output and output == 'Clean completed' or 'Terminating' in output:
            result = True
            break
        elif output:
            print(output)
        rc = webots_process.poll()
    
    print('La cosa esta ha terminado')
    assert result
    # De momento se ejecuta webots eternamente. Se detiene cerrando la ventana de webots.
    """
    webots_process.terminate()
    webots_process.wait()
    """
    #os.remove(map_file)




@given(
    objects_to_add=lists(lists(floats(0, 0.99), min_size=3, max_size=3), min_size=config_test.MIN_NUM_OBJECTS, max_size=config_test.MAX_NUM_OBJECTS),
    N=integers(8, 20),
    M=integers(8, 20)
)
@settings(
    deadline=timedelta(milliseconds=10*1000), 
    max_examples=1, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    #verbosity=Verbosity.verbose
)
def random_size(objects_to_add, N, M):
    global NUM_EXAMPLE
    global start_time
    assume(len(objects_to_add) * 3 <  N * M)
    print(N, M)
    
    if not start_time:
        start_time = time.time()

    world = World(N, M, config.TEMPLATE_PATH)

    print('Objects')
    for i, x, y in objects_to_add:
        num_possible_objects = len(list(config.POSSIBLE_OBJECTS.keys()))
        i = int(i * num_possible_objects)
        x = int(x * N * 10)
        y = int(y * M * 10)

        object_to_add = list(config.POSSIBLE_OBJECTS.keys())[i]
        
        print(x, y)
        assume(world.check_space(object_to_add, x, y, 0))
        world.add_element_with_translation(object_to_add, x, y)

    map_file = config.TEST_MAP_PATH.replace('.wbt', '{}.wbt'.format(NUM_EXAMPLE))
    world.jinja_template.stream(elements=world.objects, N=N, M=M).dump(map_file)
    NUM_EXAMPLE += 1

    print('Execution time with {} objects:'.format(len(objects_to_add)), time.time() - start_time)
    start_time = None

    command = 'webots {}'.format(map_file)
    webots_process = subprocess.Popen(
        command.split(), 
        stdout=subprocess.PIPE, 
        shell=True
    )

    # De momento se ejecuta webots eternamente. Se detiene cerrando la ventana de webots.
    """
    webots_process.terminate()
    webots_process.wait()
    """
    #os.remove(map_file)



@composite
def strategy_grid_room(draw, len_xs=0):
    """
    It generates a grid and adds an object into different places. 
    """
    xs = []
    if not len_xs:
        len_xs = draw(integers(config_test.MIN_NUM_OBJECTS, config_test.MAX_NUM_OBJECTS))

    if not N or not M:
        N = draw(integers(config_test.MIN_MAP_SIZE, config_test.MAX_MAP_SIZE))
        M = draw(integers(config_test.MIN_MAP_SIZE, config_test.MAX_MAP_SIZE))
    
    num_of_sections = get_num_of_sections(len_xs)

    init = 0 #- (N / 2)
    sections_x = []
    for i in range(num_of_sections):
        sections_x.append((init + (i * N /num_of_sections), init + ((i+1) * N / num_of_sections)))


    init = 0 #- (M / 2)
    sections_y = []
    for i in range(num_of_sections):
        sections_y.append((init + (i * M /num_of_sections), init + ((i+1) * M / num_of_sections)))
    
    map_sections = []
    for x in sections_x:
        for y in sections_y:
            map_sections.append((x, y))


    x = 0
    y = 0
    for _ in range(len_xs):
        section_to_add = draw(integers(min_value=0, max_value=len(map_sections)-1))

        add_x, add_y = map_sections.pop(section_to_add)

        x = draw(floats(min_value=add_x[0], max_value=add_x[1]))
        y = draw(floats(min_value=add_y[0], max_value=add_y[1]))
        i = draw(integers(min_value=0, max_value=99))
        xs.append((i, x, y))
        
    return (xs, N, M)


@settings(
    deadline=timedelta(milliseconds=10*1000), 
    max_examples=1, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    #verbosity=Verbosity.verbose
)
@given(input_data=strategy_grid_room())
def test_composite_iterative(input_data):
    """
    Test that take more efficient parameters. It calls to strategy_grid_room() to take the input data
    """
    global NUM_EXAMPLE
    global start_time

    objects_to_add, N, M = input_data
    
    
    assume(len(objects_to_add) * 3 <  N * M)
    if not start_time:
        start_time = time.time()

    world = World(N, M, config.TEMPLATE_PATH)

    for i, x, y in objects_to_add:
        num_possible_objects = len(list(config.POSSIBLE_OBJECTS.keys()))
        i = int(i % num_possible_objects)
        x = int(y * 10) #int(x + N / 2) * 10
        y = int(y * 10) #int(y + M / 2) * 10

        object_to_add = list(config.POSSIBLE_OBJECTS.keys())[i]

        assume(world.check_space(object_to_add, x, y, 0))
        world.add_element_with_translation(object_to_add, x, y)

    map_file = config.TEST_MAP_PATH.replace('.wbt', '{}.wbt'.format(NUM_EXAMPLE))
    world.jinja_template.stream(elements=world.objects, N=N, M=M).dump(map_file)
    NUM_EXAMPLE += 1

    print('Execution time with {} objects:'.format(len(objects_to_add)), time.time() - start_time)
    start_time = None

    command = 'webots {}'.format(map_file)
    webots_process = subprocess.Popen(
        command.split(), 
        stdout=subprocess.PIPE, 
        shell=True
    )


if __name__ == "__main__":
    #adding_multiples_elements_target_1()
    #random_size()
    test_composite_iterative()