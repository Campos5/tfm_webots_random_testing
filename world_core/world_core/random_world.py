import argparse
import jinja2
import json
import random
import subprocess
import time

class World:
    
    def __init__(self, n, m, template_path):
        self.n = n
        self.m = m
        self.objects = []
        self.room = [0 for i in range(n)]
        for i in range(n):
            self.room[i] = [0 for i in range(m)]
            
        self.num_elements = 0
        with open('webots/objects/objects.json', 'r') as f:
            self.possible_objects = json.load(f)

        with open(template_path, 'r') as template_file:
            template = template_file.read()

        self.jinja_template = jinja2.Template(template)


    def set_room_borders(self):
        # Establish as 1 the borders of the room
        
        self.room


    def mark_ocuped_space(self, object_to_add, x, y):
        # Set as 1 the space ocuped by the object
        
        self.room


    def check_space(self, object_to_add, x, y, z):
        # Check if these coordenates are available in the room
        
        self.room
        
        return True


    def get_possible_random_possition(self, object_to_add):
        # Return X and Y translation where set the object
        self.room
        free_space = False
        
        while not free_space:
            x = (random.random() * self.n) - (self.n/2)
            y = (random.random() * self.m) - (self.m/2)
            z = 0
            free_space = self.check_space(object_to_add, x, y, z)
        self.mark_ocuped_space(object_to_add, x, y)
        
        return x, y, z


    def add_element(self, possible_objects, objects):    
        object_to_add = random.choice(list(possible_objects.keys()))
        
        x, y, z = self.get_possible_random_possition(object_to_add)
        print(x,y,x)
        self.objects.append({
            'furniture': object_to_add,
            'features': 'translation {x} {z} {y}\n {size} \n\t rotation 0 0 0 0'.format(
                    x=x, y=y, z=z,
                    size=possible_objects[object_to_add].get('sizes', '')
                ),
            'name': 'obj{}'.format(self.num_elements)
        })
        self.num_elements += 1


    def add_element_with_translation(self, possible_objects, objects, x, y):
        z = 0
        object_to_add = random.choice(list(possible_objects.keys()))
        self.objects.append({
            'furniture': object_to_add,
            'features': 'translation {x} {z} {y}\n {size} \n\t rotation 0 0 0 0'.format(
                    x=x, y=y, z=z,
                    size=possible_objects[object_to_add].get('sizes', '')
                ),
            'name': 'obj{}'.format(self.num_elements)
        })
        self.num_elements += 1