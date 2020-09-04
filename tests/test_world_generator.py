import argparse
import csv
import os
import time

from hypothesis import given, settings, assume, HealthCheck, target, Verbosity, Phase
from hypothesis.strategies import integers, floats, lists, composite
from hypothesis.errors import Unsatisfiable
from datetime import timedelta
from time import sleep

import config_test
from world_core import config
from world_core.random_world import World

NUM_EXAMPLE = 0
start_time = None
num_objects = None

result_normal = []
result_target_1 = []
result_target_2 = []
result_grid = []
result_grid_no_shrink = []
result_composite = []


def distance_between_two_points(x, y):
    import math
    return math.sqrt((x[1] - x[0])**2 + (y[1] - y[0])**2)  


def get_num_of_sections(num_objects):
    import math
    x = math.sqrt(num_objects)
    return math.ceil(x)


@composite
def strategy_grid_room(draw, len_xs=0, N=0, M=0):
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


# Test functions called with parameters already treated.

def test_normal(input_data, pos):
    global NUM_EXAMPLE
    global start_time
    global result_normal
    
    objects_to_add, N, M = input_data
    
    if not start_time:
        start_time = time.time()

    world = World(N, M, config.TEMPLATE_PATH)

    for i, x, y in objects_to_add:
        num_possible_objects = len(list(config.POSSIBLE_OBJECTS.keys()))
        i = int(i * num_possible_objects)
        x = int(x * N * 10)
        y = int(y * M * 10)
        object_to_add = list(config.POSSIBLE_OBJECTS.keys())[i]
        
        assume(world.check_space(object_to_add, x, y, 0))
        world.add_element_with_translation(object_to_add, x, y)

    result_normal[pos].append(time.time() - start_time)
    NUM_EXAMPLE += 1
    start_time = None
    
    return test_shrink
    return True


def test_normal_no_shrink(input_data, pos):
    global NUM_EXAMPLE
    global start_time
    global result_normal_no_shrink
    
    objects_to_add, N, M = input_data
    
    if not start_time:
        start_time = time.time()

    world = World(N, M, config.TEMPLATE_PATH)

    for i, x, y in objects_to_add:
        num_possible_objects = len(list(config.POSSIBLE_OBJECTS.keys()))
        i = int(i * num_possible_objects)
        x = int(x * N * 10)
        y = int(y * M * 10)
        object_to_add = list(config.POSSIBLE_OBJECTS.keys())[i]
        
        assume(world.check_space(object_to_add, x, y, 0))
        world.add_element_with_translation(object_to_add, x, y)

    result_normal_no_shrink[pos].append(time.time() - start_time)
    NUM_EXAMPLE += 1
    start_time = None
    
    return test_shrink
    return True
      

def test_composite(input_data, pos):
    """
    All test composit calls to this function with diferent input
    """
    global NUM_EXAMPLE
    global start_time
    global result_grid

    objects_to_add, N, M = input_data
    
    
    assume(len(objects_to_add) * 3 <  N * M)
    if not start_time:
        start_time = time.time()

    world = World(N, M, config.TEMPLATE_PATH)

    for i, x, y in objects_to_add:
        num_possible_objects = len(list(config.POSSIBLE_OBJECTS.keys()))
        i = int(i % num_possible_objects)
        x = int(x * 10) #int(x + N / 2) * 10
        y = int(y * 10) #int(y + M / 2) * 10

        object_to_add = list(config.POSSIBLE_OBJECTS.keys())[i]

        assume(world.check_space(object_to_add, x, y, 0))
        world.add_element_with_translation(object_to_add, x, y)
    
    result_grid[pos].append(time.time() - start_time)
    NUM_EXAMPLE += 1
    start_time = None
    
    return True


def test_composite_no_shrink(input_data, pos):
    """
    All test composit calls to this function with diferent input
    """
    global NUM_EXAMPLE
    global start_time
    global result_grid_no_shrink

    objects_to_add, N, M = input_data
    
    
    assume(len(objects_to_add) * 3 <  N * M)
    if not start_time:
        start_time = time.time()

    world = World(N, M, config.TEMPLATE_PATH)

    for i, x, y in objects_to_add:
        num_possible_objects = len(list(config.POSSIBLE_OBJECTS.keys()))
        i = int(i % num_possible_objects)
        x = int(x * 10) #int(x + N / 2) * 10
        y = int(y * 10) #int(y + M / 2) * 10

        object_to_add = list(config.POSSIBLE_OBJECTS.keys())[i]

        assume(world.check_space(object_to_add, x, y, 0))
        world.add_element_with_translation(object_to_add, x, y)
    
    result_grid_no_shrink[pos].append(time.time() - start_time)
    NUM_EXAMPLE += 1
    start_time = None
    
    return True


def test_target_1(input_data, pos):
    global NUM_EXAMPLE
    global start_time
    global result_target_1
    
    objects_to_add, N, M = input_data
    
    if not start_time:
        start_time = time.time()

    world = World(N, M, config.TEMPLATE_PATH)

    # Target maximizing distance between all point
    total_distance = 0.0
    for i, x1, y1 in objects_to_add:
        for j, x2, y2 in objects_to_add:
                total_distance +=distance_between_two_points((x1, y1), (x2, y2))
                
    target(float(total_distance), label="total_distance")

    for i, x, y in objects_to_add:
        num_possible_objects = len(list(config.POSSIBLE_OBJECTS.keys()))
        i = int(i * num_possible_objects)
        x = int(x * N * 10)
        y = int(y * M * 10)
        
        object_to_add = list(config.POSSIBLE_OBJECTS.keys())[i]
        assume(world.check_space(object_to_add, x, y, 0))
        world.add_element_with_translation(object_to_add, x, y)

    result_target_1[pos].append(time.time() - start_time)
    NUM_EXAMPLE += 1
    start_time = None

    return True


def test_target_1_no_shrink(input_data, pos):
    global NUM_EXAMPLE
    global start_time
    global result_target_1_no_shrink
    
    objects_to_add, N, M = input_data
    
    if not start_time:
        start_time = time.time()

    world = World(N, M, config.TEMPLATE_PATH)

    # Target maximizing distance between all point
    total_distance = 0.0
    for i, x1, y1 in objects_to_add:
        for j, x2, y2 in objects_to_add:
                total_distance +=distance_between_two_points((x1, y1), (x2, y2))
                
    target(float(total_distance), label="total_distance")

    for i, x, y in objects_to_add:
        num_possible_objects = len(list(config.POSSIBLE_OBJECTS.keys()))
        i = int(i * num_possible_objects)
        x = int(x * N * 10)
        y = int(y * M * 10)
        
        object_to_add = list(config.POSSIBLE_OBJECTS.keys())[i]
        assume(world.check_space(object_to_add, x, y, 0))
        world.add_element_with_translation(object_to_add, x, y)

    result_target_1_no_shrink[pos].append(time.time() - start_time)
    NUM_EXAMPLE += 1
    start_time = None

    return True




def test_target_2(input_data, pos):
    global NUM_EXAMPLE
    global start_time
    global result_target_2
    
    objects_to_add, N, M = input_data
    
    if not start_time:
        start_time = time.time()

    world = World(N, M, config.TEMPLATE_PATH)

    # Target maximizing distance between all point
    total_distance = 0.0
    for i, x1, y1 in objects_to_add:
        for j, x2, y2 in objects_to_add:
                total_distance +=distance_between_two_points((x1, y1), (x2, y2))
                
    target(float(total_distance), label="total_distance")

    for i, x, y in objects_to_add:
        num_possible_objects = len(list(config.POSSIBLE_OBJECTS.keys()))
        i = int(i * num_possible_objects)
        x = int(x * N * 10)
        y = int(y * M * 10)
        object_to_add = list(config.POSSIBLE_OBJECTS.keys())[i]
        
        assume(world.check_space(object_to_add, x, y, 0))
        world.add_element_with_translation(object_to_add, x, y)

    result_target_2[pos].append(time.time() - start_time)
    NUM_EXAMPLE += 1
    start_time = None

    return True


def test_target_2_no_shrink(input_data, pos):
    global NUM_EXAMPLE
    global start_time
    global result_target_2_no_shrink
    
    objects_to_add, N, M = input_data
    
    if not start_time:
        start_time = time.time()

    world = World(N, M, config.TEMPLATE_PATH)

    # Target maximizing distance between all point
    total_distance = 0.0
    for i, x1, y1 in objects_to_add:
        for j, x2, y2 in objects_to_add:
                total_distance +=distance_between_two_points((x1, y1), (x2, y2))
                
    target(float(total_distance), label="total_distance")

    for i, x, y in objects_to_add:
        num_possible_objects = len(list(config.POSSIBLE_OBJECTS.keys()))
        i = int(i * num_possible_objects)
        x = int(x * N * 10)
        y = int(y * M * 10)
        object_to_add = list(config.POSSIBLE_OBJECTS.keys())[i]
        
        assume(world.check_space(object_to_add, x, y, 0))
        world.add_element_with_translation(object_to_add, x, y)

    result_target_2_no_shrink[pos].append(time.time() - start_time)
    NUM_EXAMPLE += 1
    start_time = None

    return True


##########       TEST TO MAP GENERATOR       ############



@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=5, max_size=5)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
def test_normal_map_generator_10x10_with_5_no_shrink(objects_to_add):
    input_data = (objects_to_add, 10, 10)
    assert test_normal_no_shrink(input_data, 0)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=7, max_size=7)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
def test_normal_map_generator_10x10_with_7_no_shrink(objects_to_add):
    input_data = (objects_to_add, 10, 10)
    assert test_normal_no_shrink(input_data, 1)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=10, max_size=10)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
def test_normal_map_generator_10x10_with_10_no_shrink(objects_to_add):
    input_data = (objects_to_add, 10, 10)
    assert test_normal_no_shrink(input_data, 2)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=12, max_size=12)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
def test_normal_map_generator_10x10_with_12_no_shrink(objects_to_add):
    input_data = (objects_to_add, 10, 10)
    assert test_normal_no_shrink(input_data, 3)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=15, max_size=15)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
def test_normal_map_generator_10x10_with_15_no_shrink(objects_to_add):
    input_data = (objects_to_add, 10, 10)
    assert test_normal_no_shrink(input_data, 4)






# Test with 10x10 room and different number of objects. Normal generation.

@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=5, max_size=5)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_normal_map_generator_10x10_with_5(objects_to_add):
    input_data = (objects_to_add, 10, 10)
    result =  test_normal(input_data, 0)
    assert result


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=7, max_size=7)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_normal_map_generator_10x10_with_7(objects_to_add):
    input_data = (objects_to_add, 10, 10)
    assert test_normal(input_data, 1)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=10, max_size=10)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_normal_map_generator_10x10_with_10(objects_to_add):
    input_data = (objects_to_add, 10, 10)
    assert test_normal(input_data, 2)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=12, max_size=12)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_normal_map_generator_10x10_with_12(objects_to_add):
    input_data = (objects_to_add, 10, 10)
    assert test_normal(input_data, 3)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=15, max_size=15)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_normal_map_generator_10x10_with_15(objects_to_add):
    input_data = (objects_to_add, 10, 10)
    assert test_normal(input_data, 4)


# Test with 10x10 room and different number of objects. Using target function.
# There are two target functions, maximizing the distance between one object and the next one,
# and maximizing the sumatory oo all distances.
# The function with better result will be used to test later. 

@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=5, max_size=5)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_1_10x10_with_5(objects_to_add):
    input_data = (objects_to_add, 10, 10)
    assert test_target_1(input_data, 0)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=7, max_size=7)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_1_10x10_with_7(objects_to_add):
    input_data = (objects_to_add, 10, 10)
    assert test_target_1(input_data, 1)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=10, max_size=10)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_1_10x10_with_10(objects_to_add):
    input_data = (objects_to_add, 10, 10)
    assert test_target_1(input_data, 2)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=12, max_size=12)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_1_10x10_with_12(objects_to_add):
    input_data = (objects_to_add, 10, 10)
    assert test_target_1(input_data, 3)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=15, max_size=15)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_1_10x10_with_15(objects_to_add):
    input_data = (objects_to_add, 10, 10)
    assert test_target_1(input_data, 4)


# Second target function

@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=5, max_size=5)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_2_10x10_with_5(objects_to_add):
    input_data = (objects_to_add, 10, 10)
    assert test_target_2(input_data, 0)
    

@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=7, max_size=7)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_2_10x10_with_7(objects_to_add):
    input_data = (objects_to_add, 10, 10)
    assert test_target_2(input_data, 1)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=10, max_size=10)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_2_10x10_with_10(objects_to_add):
    input_data = (objects_to_add, 10, 10)
    assert test_target_2(input_data, 2)
    

@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=12, max_size=12)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_2_10x10_with_12(objects_to_add):
    input_data = (objects_to_add, 10, 10)
    assert test_target_2(input_data, 3)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=15, max_size=15)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_2_10x10_with_15(objects_to_add):
    input_data = (objects_to_add, 10, 10)
    assert test_target_2(input_data, 4)    

# Test with 10x10 room and different number of objects. Using composite function (grid room).

@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
@given(input_data=strategy_grid_room(len_xs=5, N=10, M=10))
def test_composite_10x10_with_5(input_data):
    assert test_composite(input_data, 0)


@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
@given(input_data=strategy_grid_room(len_xs=7, N=10, M=10))
def test_composite_10x10_with_7(input_data):
    assert test_composite(input_data, 1)


@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
@given(input_data=strategy_grid_room(len_xs=10, N=10, M=10))
def test_composite_10x10_with_10(input_data):
    assert test_composite(input_data, 2)


@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
@given(input_data=strategy_grid_room(len_xs=12, N=10, M=10))
def test_composite_10x10_with_12(input_data):
    assert test_composite(input_data, 3)



@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
@given(input_data=strategy_grid_room(len_xs=15, N=10, M=10))
def test_composite_10x10_with_15(input_data):
    assert test_composite_no_shrink(input_data, 4)


# Grid test no shrink


@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
@given(input_data=strategy_grid_room(len_xs=5, N=10, M=10))
def test_composite_10x10_with_5_no_shrink(input_data):
    assert test_composite_no_shrink(input_data, 0)


@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
@given(input_data=strategy_grid_room(len_xs=7, N=10, M=10))
def test_composite_10x10_with_7_no_shrink(input_data):
    assert test_composite_no_shrink(input_data, 1)


@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
@given(input_data=strategy_grid_room(len_xs=10, N=10, M=10))
def test_composite_10x10_with_10_no_shrink(input_data):
    assert test_composite_no_shrink(input_data, 2)


@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
@given(input_data=strategy_grid_room(len_xs=12, N=10, M=10))
def test_composite_10x10_with_12_no_shrink(input_data):
    assert test_composite_no_shrink(input_data, 3)



@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
@given(input_data=strategy_grid_room(len_xs=15, N=10, M=10))
def test_composite_10x10_with_15_no_shrink(input_data):
    assert test_composite_no_shrink(input_data, 4)


# Test with 10 objects and different room size. Using different functions.


# NORMAL FUNCTION

@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=10, max_size=10)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_normal_map_generator_10x14_with_10(objects_to_add):
    input_data = (objects_to_add, 10, 14)
    assert test_normal(input_data, 0)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=10, max_size=10)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_normal_map_generator_10x17_with_10(objects_to_add):
    input_data = (objects_to_add, 10, 17)
    assert test_normal(input_data, 1)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=10, max_size=10)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_normal_map_generator_10x20_with_10(objects_to_add):
    input_data = (objects_to_add, 10, 20)
    assert test_normal(input_data, 2)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=10, max_size=10)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_normal_map_generator_15x15_with_10(objects_to_add):
    input_data = (objects_to_add, 15, 15)
    assert test_normal(input_data, 3)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=10, max_size=10)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_normal_map_generator_20x20_with_10(objects_to_add):
    input_data = (objects_to_add, 20, 20)
    assert test_normal(input_data, 4)



# TEST TARGET 1


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=10, max_size=10)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_1_map_generator_10x14_with_10(objects_to_add):
    input_data = (objects_to_add, 10, 14)
    assert test_target_1(input_data, 0)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=10, max_size=10)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_1_map_generator_10x17_with_10(objects_to_add):
    input_data = (objects_to_add, 10, 17)
    assert test_target_1(input_data, 1)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=10, max_size=10)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_1_map_generator_10x20_with_10(objects_to_add):
    input_data = (objects_to_add, 10, 20)
    assert test_target_1(input_data, 2)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=10, max_size=10)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_1_map_generator_15x15_with_10(objects_to_add):
    input_data = (objects_to_add, 15, 15)
    assert test_target_1(input_data, 3)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=10, max_size=10)
)
@settings(
    deadline=timedelta(milliseconds=10*60*1000), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_1_map_generator_20x20_with_10(objects_to_add):
    input_data = (objects_to_add, 20, 20)
    assert test_target_1(input_data, 4)


# TEST TARGET 2


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=10, max_size=10)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_2_map_generator_10x14_with_10(objects_to_add):
    input_data = (objects_to_add, 10, 14)
    assert test_target_2(input_data, 0)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=10, max_size=10)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_2_map_generator_10x17_with_10(objects_to_add):
    input_data = (objects_to_add, 10, 17)
    assert test_target_2(input_data, 1)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=10, max_size=10)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_2_map_generator_10x20_with_10(objects_to_add):
    input_data = (objects_to_add, 10, 20)
    assert test_target_2(input_data, 2)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=10, max_size=10)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_2_map_generator_15x15_with_10(objects_to_add):
    input_data = (objects_to_add, 15, 15)
    assert test_target_2(input_data, 3)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=10, max_size=10)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_2_map_generator_20x20_with_10(objects_to_add):
    input_data = (objects_to_add, 20, 20)
    assert test_target_2(input_data, 4)


# TEST COMPOSITE

@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
@given(input_data=strategy_grid_room(len_xs=10, N=10, M=14))
def test_composite_map_generator_10x14_with_10(input_data):
    assert test_composite(input_data, 0)


@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
@given(input_data=strategy_grid_room(len_xs=10, N=10, M=17))
def test_composite_map_generator_10x17_with_10(input_data):
    assert test_composite(input_data, 1)


@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
@given(input_data=strategy_grid_room(len_xs=10, N=10, M=20))
def test_composite_map_generator_10x20_with_10(input_data):
    assert test_composite(input_data, 2)


@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
@given(input_data=strategy_grid_room(len_xs=10, N=15, M=15))
def test_composite_map_generator_15x15_with_10(input_data):
    assert test_composite(input_data, 3)


@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
@given(input_data=strategy_grid_room(len_xs=10, N=20, M=20))
def test_composite_map_generator_20x20_with_10(input_data):
    assert test_composite(input_data, 4)


# TEST COMPOSITE no shrink

@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
@given(input_data=strategy_grid_room(len_xs=10, N=10, M=14))
def test_composite_map_generator_10x14_with_10_no_shrink(input_data):
    assert test_composite_no_shrink(input_data, 0)


@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
@given(input_data=strategy_grid_room(len_xs=10, N=10, M=17))
def test_composite_map_generator_10x17_with_10_no_shrink(input_data):
    assert test_composite_no_shrink(input_data, 1)


@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
@given(input_data=strategy_grid_room(len_xs=10, N=10, M=20))
def test_composite_map_generator_10x20_with_10_no_shrink(input_data):
    assert test_composite_no_shrink(input_data, 2)


@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
@given(input_data=strategy_grid_room(len_xs=10, N=15, M=15))
def test_composite_map_generator_15x15_with_10_no_shrink(input_data):
    assert test_composite_no_shrink(input_data, 3)



@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
@given(input_data=strategy_grid_room(len_xs=10, N=20, M=20))
def test_composite_map_generator_20x20_with_10_no_shrink(input_data):
    assert test_composite_no_shrink(input_data, 4)



# All random parameters and different functions.

@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=config_test.MIN_NUM_OBJECTS, max_size=config_test.MAX_NUM_OBJECTS),
    N=integers(config_test.MIN_MAP_SIZE,config_test.MAX_MAP_SIZE),
    M=integers(config_test.MIN_MAP_SIZE,config_test.MAX_MAP_SIZE)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_normal_map_generator_all_random(objects_to_add, N, M):
    input_data = (objects_to_add, N, M)
    assert test_normal(input_data, 0)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=config_test.MIN_NUM_OBJECTS, max_size=config_test.MAX_NUM_OBJECTS),
    N=integers(config_test.MIN_MAP_SIZE,config_test.MAX_MAP_SIZE),
    M=integers(config_test.MIN_MAP_SIZE,config_test.MAX_MAP_SIZE)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_normal_map_generator_all_random_no_shrink(objects_to_add, N, M):
    input_data = (objects_to_add, N, M)
    assert test_normal_no_shrink(input_data, 0)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=config_test.MIN_NUM_OBJECTS, max_size=config_test.MAX_NUM_OBJECTS),
    N=integers(config_test.MIN_MAP_SIZE,config_test.MAX_MAP_SIZE),
    M=integers(config_test.MIN_MAP_SIZE,config_test.MAX_MAP_SIZE)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_1_map_generator_all_random(objects_to_add, N, M):
    input_data = (objects_to_add, N, M)
    assert test_target_1(input_data, 0)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=config_test.MIN_NUM_OBJECTS, max_size=config_test.MAX_NUM_OBJECTS),
    N=integers(config_test.MIN_MAP_SIZE,config_test.MAX_MAP_SIZE),
    M=integers(config_test.MIN_MAP_SIZE,config_test.MAX_MAP_SIZE)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_1_map_generator_all_random_no_shrink(objects_to_add, N, M):
    input_data = (objects_to_add, N, M)
    assert test_target_1_no_shrink(input_data, 0)



@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=config_test.MIN_NUM_OBJECTS, max_size=config_test.MAX_NUM_OBJECTS),
    N=integers(config_test.MIN_MAP_SIZE,config_test.MAX_MAP_SIZE),
    M=integers(config_test.MIN_MAP_SIZE,config_test.MAX_MAP_SIZE)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_2_map_generator_all_random(objects_to_add, N, M):
    input_data = (objects_to_add, N, M)
    assert test_target_2(input_data, 0)


@given(
    objects_to_add=lists(lists(floats(0.0, 0.99), min_size=3, max_size=3), min_size=config_test.MIN_NUM_OBJECTS, max_size=config_test.MAX_NUM_OBJECTS),
    N=integers(config_test.MIN_MAP_SIZE,config_test.MAX_MAP_SIZE),
    M=integers(config_test.MIN_MAP_SIZE,config_test.MAX_MAP_SIZE)
)
@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
def test_target_2_map_generator_all_random_no_shrink(objects_to_add, N, M):
    input_data = (objects_to_add, N, M)
    assert test_target_2_no_shrink(input_data, 0)



@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,),
    phases=[Phase.explicit, Phase.reuse, Phase.generate]
)
@given(input_data=strategy_grid_room())
def test_composite_map_generator_all_random(input_data):
    assert test_composite(input_data, 0)


@settings(
    deadline=timedelta(milliseconds=config_test.DEADLINE), 
    max_examples=1000, 
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow,)
)
@given(input_data=strategy_grid_room())
def test_composite_map_generator_no_shrink_all_random(input_data):
    assert test_composite_no_shrink(input_data, 0)



def test_10x10(directory):
    global NUM_EXAMPLE
    global result_normal
    global result_target_1
    global result_target_2
    global result_grid
    global result_grid_no_shrink

    result_normal = [[] for i in range(5)]
    result_target_1 = [[] for i in range(5)]
    result_target_2 = [[] for i in range(5)]
    result_grid = [[] for i in range(5)]
    result_grid_no_shrink = [[] for i in range(5)]
    
    
    num_examples_normal = []
    num_examples_target_1 = []
    num_examples_target_2 = []
    num_examples_grid = []
    num_examples_grid_no_shrink = []
    
    init_time = time.time()

    try:
        test_normal_map_generator_10x10_with_5()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_normal.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    try:
        test_normal_map_generator_10x10_with_7()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_normal.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    try:
        test_normal_map_generator_10x10_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_normal.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    try:
        test_normal_map_generator_10x10_with_12()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_normal.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    try:
        test_normal_map_generator_10x10_with_15()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_normal.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    with open(os.path.join(directory, 'test_result_normal-10x10.csv'), 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for row, i, x in zip(result_normal, [5,7,10,12,15], num_examples_normal):
            wr.writerow(['Num_objects: {}'.format(i)] + ['Num_examples: {}'.format(x)] + row)

    print('Normal CSV ready')

    try:
        test_target_1_10x10_with_5()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_target_1.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    try:
        test_target_1_10x10_with_7()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_target_1.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    try:
        test_target_1_10x10_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_target_1.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    try:
        test_target_1_10x10_with_12()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_target_1.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    try:
        test_target_1_10x10_with_15()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_target_1.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    with open(os.path.join(directory, 'test_result_target_1-10x10.csv'), 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for row, i, x in zip(result_target_1, [5,7,10,12,15], num_examples_target_1):
            wr.writerow(['Num_objects: {}'.format(i)] + ['Num_examples: {}'.format(x)] + row)
    
    print('Target 1 CSV ready')
    

    try:
        test_target_2_10x10_with_5()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_target_2.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    try:
        test_target_2_10x10_with_7()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_target_2.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    try:
        test_target_2_10x10_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_target_2.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    try:
        test_target_2_10x10_with_12()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_target_2.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    try:
        test_target_2_10x10_with_15()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_target_2.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    with open(os.path.join(directory, 'test_result_target_2-10x10.csv'), 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for row, i, x in zip(result_target_2, [5,7,10,12,15], num_examples_target_2):
            wr.writerow(['Num_objects: {}'.format(i)] + ['Num_examples: {}'.format(x)] + row)
    
    print('Target 2 CSV ready')


    try:
        test_composite_10x10_with_5()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_grid.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    try:
        test_composite_10x10_with_7()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_grid.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    try:
        test_composite_10x10_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_grid.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    try:
        test_composite_10x10_with_12()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_grid.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    try:
        test_composite_10x10_with_15()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_grid.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    with open(os.path.join(directory, 'test_result_grid-10x10.csv'), 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for row, i, x in zip(result_grid, [5,7,10,12,15], num_examples_grid):
            wr.writerow(['Num_objects: {}'.format(i)] + ['Num_examples: {}'.format(x)] + row)
    
    print('Grid CSV ready')
    
    
    try:
        test_composite_10x10_with_5_no_shrink()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_grid_no_shrink.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    try:
        test_composite_10x10_with_7_no_shrink()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_grid_no_shrink.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    try:
        test_composite_10x10_with_10_no_shrink()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_grid_no_shrink.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    try:
        test_composite_10x10_with_12_no_shrink()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_grid_no_shrink.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0
    
    try:
        test_composite_10x10_with_15_no_shrink()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    num_examples_grid_no_shrink.append(NUM_EXAMPLE)
    NUM_EXAMPLE = 0

    with open(os.path.join(directory, 'test_result_grid_no_shrink-10x10.csv'), 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for row, i in zip(result_grid_no_shrink, [5,7,10,12,15]):
            wr.writerow(['Num_objects: {}'.format(i)] + ['Num_examples: {}'.format(len(row))] + row)
    
    print('Grid no shrink CSV ready')
    print('Execution time test 10x10', time.time() - init_time)


def test_10_objects(directory):
    global result_normal
    global result_target_1
    global result_target_2
    global result_grid
    global result_grid_no_shrink

    result_normal = [[] for i in range(5)]
    result_target_1 = [[] for i in range(5)]
    result_target_2 = [[] for i in range(5)]
    result_grid = [[] for i in range(5)]
    result_grid_no_shrink = [[] for i in range(5)]
    
    init_time = time.time()

    try:
        test_normal_map_generator_10x14_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    try:
        test_normal_map_generator_10x17_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    
    try:
        test_normal_map_generator_10x20_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    
    try:
        test_normal_map_generator_15x15_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    
    try:
        test_normal_map_generator_20x20_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    
    with open(os.path.join(directory, 'test_result_normal-10_objects.csv'), 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for row, i in zip(result_normal, ['10x14', '10x17', '10x20', '15x15', '20x20']):
            wr.writerow(['Room_size: {}'.format(i)] + ['Num_examples: {}'.format(len(row))] + row)

    print('Normal CSV ready')

    try:
        test_target_1_map_generator_10x14_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    try:
        test_target_1_map_generator_10x17_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    
    try:
        test_target_1_map_generator_10x20_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    
    try:
        test_target_1_map_generator_15x15_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    
    try:
        test_target_1_map_generator_20x20_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    
    with open(os.path.join(directory, 'test_result_target_1-10_objects.csv'), 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for row, i in zip(result_target_1, ['10x14', '10x17', '10x20', '15x15', '20x20']):
            wr.writerow(['Room_size: {}'.format(i)] + ['Num_examples: {}'.format(len(row))] + row)

    print('Target 1 CSV ready')


    try:
        test_target_2_map_generator_10x14_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    try:
        test_target_2_map_generator_10x17_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    
    try:
        test_target_2_map_generator_10x20_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    
    try:
        test_target_2_map_generator_15x15_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    
    try:
        test_target_2_map_generator_20x20_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    
    with open(os.path.join(directory, 'test_result_target_2-10_objects.csv'), 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for row, i in zip(result_target_2, ['10x14', '10x17', '10x20', '15x15', '20x20']):
            wr.writerow(['Room_size: {}'.format(i)] + ['Num_examples: {}'.format(len(row))] + row)

    print('Target 2 CSV ready')

    try:
        test_composite_map_generator_10x14_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    try:
        test_composite_map_generator_10x17_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    
    try:
        test_composite_map_generator_10x20_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    
    try:
        test_composite_map_generator_15x15_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    
    try:
        test_composite_map_generator_20x20_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    
    with open(os.path.join(directory, 'test_result_composite-10_objects.csv'), 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for row, i in zip(result_grid, ['10x14', '10x17', '10x20', '15x15', '20x20']):
            wr.writerow(['Room_size: {}'.format(i)] + ['Num_examples: {}'.format(len(row))] + row)

    print('Grid CSV ready')


    try:
        test_composite_map_generator_10x14_with_10_no_shrink()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    try:
        test_composite_map_generator_10x17_with_10_no_shrink()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    
    try:
        test_composite_map_generator_10x20_with_10_no_shrink()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    
    try:
        test_composite_map_generator_15x15_with_10_no_shrink()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    
    try:
        test_composite_map_generator_20x20_with_10_no_shrink()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    NUM_EXAMPLE = 0
    
    with open(os.path.join(directory, 'test_result_composite_no_shrink-10_objects.csv'), 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for row, i in zip(result_grid_no_shrink, ['10x14', '10x17', '10x20', '15x15', '20x20']):
            wr.writerow(['Room_size: {}'.format(i)] + ['Num_examples: {}'.format(len(row))] + row)

    print('Grid no shrink CSV ready')

    print('Execution time test 10 objects', time.time() - init_time)


def all_random(directory):
    global result_normal
    global result_normal_no_shrink
    global result_target_1
    global result_target_1_no_shrink
    global result_target_2
    global result_target_2_no_shrink
    global result_grid
    global result_grid_no_shrink

    result_normal = [[] for i in range(1)]
    result_normal_no_shrink = [[] for i in range(1)]
    result_target_1 = [[] for i in range(1)]
    result_target_1_no_shrink = [[] for i in range(1)]
    result_target_2 = [[] for i in range(1)]
    result_target_2_no_shrink = [[] for i in range(1)]
    result_grid = [[] for i in range(1)]
    result_grid_no_shrink = [[] for i in range(1)]
    
    result_all_random = []
    
    init_time = time.time()

    try:
        test_normal_map_generator_all_random()
        result_all_random.append(result_normal[0])
    except (AssertionError,Unsatisfiable):
        pass
    
    print('Execution time test all random', time.time() - init_time)
    print('Next')
    init_time = time.time()

    try:
        test_normal_map_generator_all_random_no_shrink()
        result_all_random.append(result_normal_no_shrink[0])
    except (AssertionError,Unsatisfiable):
        pass
    
    print('Execution time test all random', time.time() - init_time)
    print('Next')
    init_time = time.time()
    
    try:
        test_target_1_map_generator_all_random()
        result_all_random.append(result_target_1[0])
    except (AssertionError,Unsatisfiable):
        pass
    
    print('Execution time test all random', time.time() - init_time)
    print('Next')
    init_time = time.time()
    
    try:
        test_target_1_map_generator_all_random_no_shrink()
        result_all_random.append(result_target_1_no_shrink[0])
    except (AssertionError,Unsatisfiable):
        pass
    
    print('Execution time test all random', time.time() - init_time)
    print('Next')
    init_time = time.time()
    
    try:
        test_target_2_map_generator_all_random()
        result_all_random.append(result_target_2[0])
    except (AssertionError,Unsatisfiable):
        pass
    
    print('Execution time test all random', time.time() - init_time)
    print('Next')
    init_time = time.time()
    
    try:
        test_target_2_map_generator_all_random_no_shrink()
        result_all_random.append(result_target_2_no_shrink[0])
    except (AssertionError,Unsatisfiable):
        pass
    
    print('Execution time test all random', time.time() - init_time)
    print('Next')
    init_time = time.time()
    
    try:
        test_composite_map_generator_all_random()
        result_all_random.append(result_grid[0])
    except (AssertionError,Unsatisfiable):
        pass

    print('Execution time test all random', time.time() - init_time)
    print('Next')
    init_time = time.time()

    try:
        test_composite_map_generator_no_shrink_all_random()
        result_all_random.append(result_grid_no_shrink[0])
    except (AssertionError,Unsatisfiable):
        pass
    
    print('Execution time test all random', time.time() - init_time)
    
    functions = ['Test normal', 'Test normal sin reduccion','Test dirigido 1', 'Test dirigido 1 sin reducción', 'Test dirigido 2', 'Test dirigido 2 sin reducción','Test compuesto', 'Test compuesto sin reducción']
    with open(os.path.join(directory, 'test_all_random.csv'), 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for row, i in zip(result_all_random, functions):
            wr.writerow(['Función: {}'.format(i)] + ['Num_examples: {}'.format(len(row))] + row)



def shrink_vs_no_shrink(directory):
    global NUM_EXAMPLE
    global result_normal
    global result_normal_no_shrink

    result_normal = [[] for i in range(5)]
    result_normal_no_shrink = [[] for i in range(5)]
    
    init_time = time.time()

    try:
        test_normal_map_generator_10x10_with_5()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    try:
        test_normal_map_generator_10x10_with_7()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    
    try:
        test_normal_map_generator_10x10_with_10()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    
    try:
        test_normal_map_generator_10x10_with_12()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    
    try:
        test_normal_map_generator_10x10_with_15()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    
    with open(os.path.join(directory, 'test_result_normal-10x10.csv'), 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for row, i in zip(result_normal, [5,7,10,12,15]):
            wr.writerow(['Num_objects: {}'.format(i)] + ['Num_examples: {}'.format(len(row))] + row)

    print('Normal CSV ready')

    try:
        test_normal_map_generator_10x10_with_5_no_shrink()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    try:
        test_normal_map_generator_10x10_with_7_no_shrink()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    
    try:
        test_normal_map_generator_10x10_with_10_no_shrink()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    
    try:
        test_normal_map_generator_10x10_with_12_no_shrink()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    
    try:
        test_normal_map_generator_10x10_with_15_no_shrink()
    except (AssertionError,Unsatisfiable):
        pass
    print('Next')
    
    with open(os.path.join(directory, 'test_result_normal_no_shrink-10x10.csv'), 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for row, i in zip(result_normal_no_shrink, [5,7,10,12,15]):
            wr.writerow(['Num_objects: {}'.format(i)] + ['Num_examples: {}'.format(len(row))] + row)

    print('Normal CSV ready')


if __name__ == "__main__":  
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--directory', type=str, required=True, help='Folder where save csvs')
    ap.add_argument('-t', '--test',  help='Add it to execute test', action='store_false')
    args = ap.parse_args()
    
    
    test_shrink = args.test
    
    #shrink_vs_no_shrink(args.directory)
    test_10x10(args.directory)
    test_10_objects(args.directory)
    all_random(args.directory)
