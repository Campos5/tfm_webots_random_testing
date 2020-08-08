import argparse
import csv
import time

from hypothesis import given, settings, assume, HealthCheck, target, Verbosity
from hypothesis.strategies import integers, floats, lists
from hypothesis.errors import Unsatisfiable
from datetime import timedelta
from time import sleep

import config_test
from world_core import config
from world_core.random_world import World

NUM_EXAMPLE = 0
start_time = None
num_objects = None


result_test_1 = []
result_test_2 = []
result_test_3 = []


def distance_between_two_points(x, y):
    import math
    return math.sqrt((x[1] - x[0])**2 + (y[1] - y[0])**2)  


##########       TEST TO MAP GENERATOR       ############

# Test with 10x10 room and different number of objects. Normal generation.

@given(
    objects_to_add=lists(lists(integers(0, 99), min_size=3, max_size=3), min_size=5, max_size=5)
)
@settings(
    deadline=timedelta(milliseconds=10*1000*60), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_normal_map_generator_with_5(objects_to_add):    
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

    
    result_test_1[0].append(time.time() - start_time)
    start_time = None

    
    assert True


@given(
    objects_to_add=lists(lists(integers(0, 99), min_size=3, max_size=3), min_size=7, max_size=7)
)
@settings(
    deadline=timedelta(milliseconds=10*1000*60), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_normal_map_generator_with_7(objects_to_add):    
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

    
    result_test_1[1].append(time.time() - start_time)
    start_time = None

    
    assert True


@given(
    objects_to_add=lists(lists(integers(0, 99), min_size=3, max_size=3), min_size=10, max_size=10)
)
@settings(
    deadline=timedelta(milliseconds=10*1000*60), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_normal_map_generator_with_10(objects_to_add):    
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

    
    result_test_1[2].append(time.time() - start_time)
    start_time = None

    
    assert True



@given(
    objects_to_add=lists(lists(integers(0, 99), min_size=3, max_size=3), min_size=12, max_size=12)
)
@settings(
    deadline=timedelta(milliseconds=10*1000*60), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_normal_map_generator_with_12(objects_to_add):    
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

    
    result_test_1[3].append(time.time() - start_time)
    start_time = None

    
    assert True


@given(
    objects_to_add=lists(lists(integers(0, 99), min_size=3, max_size=3), min_size=15, max_size=15)
)
@settings(
    deadline=timedelta(milliseconds=10*1000*60), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_normal_map_generator_with_15(objects_to_add):    
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

    
    result_test_1[4].append(time.time() - start_time)
    start_time = None

    
    assert True



# Test with 10x10 room and different number of objects. Using target function.

@given(
    objects_to_add=lists(lists(integers(0, 99), min_size=3, max_size=3), min_size=config_test.MIN_NUM_OBJECTS, max_size=config_test.MAX_NUM_OBJECTS)
)
@settings(
    deadline=timedelta(milliseconds=10*1000*60), 
    max_examples=5, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
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

    for i, x, y in objects_to_add:
        num_possible_objects = len(list(config.POSSIBLE_OBJECTS.keys()))
        object_to_add = list(config.POSSIBLE_OBJECTS.keys())[i % num_possible_objects]
        assume(world.check_space(object_to_add, x, y, 0))
        world.add_element_with_translation(object_to_add, x, y)


    assert True


@given(
    objects_to_add=lists(lists(integers(0, 99), min_size=3, max_size=3), min_size=config_test.MIN_NUM_OBJECTS, max_size=config_test.MAX_NUM_OBJECTS)
)
@settings(
    deadline=timedelta(milliseconds=10*1000*60), 
    max_examples=1, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def adding_multiples_elements_target_2(objects_to_add):    
    global NUM_EXAMPLE
    global start_time
    
    if not start_time:
        start_time = time.time()

    world = World(10, 10, config.TEMPLATE_PATH)

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

    assert True
    
    

# Test with 10x10 room and different number of objects. Using compose function (grid room).
    


# Test with X objects and different room size. Using different functions.



# All random parameters and different functions.


    
if __name__ == "__main__":
    
    result_test_1 = [[] for i in range(5)]
    result_test_2 = [[] for i in range(11)]
    result_test_3 = [[] for i in range(11)]
    
    init_time = time.time()
    
    try:
        test_normal_map_generator_with_5()
    except Unsatisfiable:
        pass
    print('Next')
    
    try:
        test_normal_map_generator_with_7()
    except Unsatisfiable:
        pass
    print('Next')
    
    try:
        test_normal_map_generator_with_10()
    except Unsatisfiable:
        pass
    print('Next')
    
    try:
        test_normal_map_generator_with_12()
    except Unsatisfiable:
        pass
    print('Next')
    
    try:
        test_normal_map_generator_with_15()
    except Unsatisfiable:
        pass
    print('Next')
    
    with open('test_result_1.csv', 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for row, i in zip(result_test_1, [5,7,10,12,15]):
            wr.writerow(['Num_objects: {}'.format(i)] + row)


    print('Execution time', time.time() - init_time)



