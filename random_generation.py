import argparse
import random
import jinja2
import json
import subprocess
import time

from hypothesis import given
from hypothesis.strategies import integers, floats

N = 10
M = 10
ROOM = [0 for i in range(N)]
for i in range(N):
    ROOM[i] = [0 for i in range(M)]

NUM_ELEMENTS = 0

def set_room_borders():
    # Establish as 1 the borders of the room
    
    global ROOM


def mark_ocuped_space(object_to_add, x, y):
    # Set as 1 the space ocuped by the object
    
    global ROOM


def check_space(object_to_add, x, y, z):
    # Check if these coordenates are available in the room
    
    global ROOM
    
    return True

def get_possible_random_possition(object_to_add):
    # Return X and Y translation where set the object
    global ROOM
    free_space = False
    
    while not free_space:
        x = (random.random() * N) - (N/2)
        y = (random.random() * M) - (M/2)
        z = 0
        free_space = check_space(object_to_add, x, y, z)
    mark_ocuped_space(object_to_add, x, y)
    
    return x, y, z


def add_element(possible_objects, objects):
    global NUM_ELEMENTS
    
    object_to_add = random.choice(list(possible_objects.keys()))
    
    x, y, z = get_possible_random_possition(object_to_add)
    print(x,y,x)
    objects.append({
        'furniture': object_to_add,
        'features': 'translation {x} {z} {y}\n {size} \n\t rotation 0 0 0 0'.format(
                x=x, y=y, z=z,
                size=possible_objects[object_to_add].get('sizes', '')
            ),
        'name': 'obj{}'.format(NUM_ELEMENTS)
    })
    NUM_ELEMENTS += 1
    return objects
 
def add_element_with_translation(possible_objects, objects, x, y):
    global NUM_ELEMENTS
    z = 0
    object_to_add = random.choice(list(possible_objects.keys()))
    objects.append({
        'furniture': object_to_add,
        'features': 'translation {x} {z} {y}\n {size} \n\t rotation 0 0 0 0'.format(
                x=x, y=y, z=z,
                size=possible_objects[object_to_add].get('sizes', '')
            ),
        'name': 'obj{}'.format(NUM_ELEMENTS)
    })
    NUM_ELEMENTS += 1
    return objects


@given(x=floats(), y=floats(), n=integers())
def test_foo(x, y, n):
    objects = []
    
    with open('webots/objects/objects.json', 'r') as f:
        possible_objects = json.load(f)

    with open('webots/maps/template_map.wbt', 'r') as template_file:
        template = template_file.read()

    jinja_template = jinja2.Template(template)

    for _ in n:
        objects = add_element_with_translation(possible_objects, objects, x, y)
        objects = add_element(possible_objects, objects)
        objects = add_element(possible_objects, objects)


    jinja_template.stream(elements=objects).dump('test.wbt')

    command = 'webots test.wbt'
    webots_process = subprocess.Popen(command.split())

    '''
    time.sleep(10)
    print('TIMEOUT')
    webots_process.terminate()
    webots_process.wait()
    '''