import argparse
import jinja2
import json
import random
import subprocess
import time

from world_core import config

class World:
    
    def __init__(self, n, m, template_path):
        self.n = n
        self.m = m
        
        self.n_big = n * 10 
        self.m_big = m * 10
        
        self.objects = []
        
        # We multiply dimensions for 10 to have more accuracy.
        
        self.room = [0 for i in range(self.n_big)]
        for i in range(self.n_big):
            self.room[i] = [0 for i in range(self.m_big)]
        self.set_room_borders()

        self.num_elements = 0
        with open(template_path, 'r') as template_file:
            template = template_file.read()

        self.jinja_template = jinja2.Template(template)


    def set_room_borders(self):
        # Establish as 1 the borders of the room
        self.room[0] = [1 for _ in range(self.m_big)]
        self.room[-1] = [1 for _ in range(self.m_big)]
        for i in range(len(self.room)):
            self.room[i][0] = 1
            self.room[i][-1] = 1


    def mark_ocuped_space(self, object_to_add, x, y):
        # Set as 1 the space ocuped by the object
        
        object_size_x = int(config.POSSIBLE_OBJECTS[object_to_add]['size']['x'] * 10) 
        object_size_y = int(config.POSSIBLE_OBJECTS[object_to_add]['size']['y'] * 10)
        
        self.room[x][y]
        for i in range(object_size_x):
            if x + i < len(self.room):
                self.room[x+i][y] = 1

            if x - i >= 0:
                self.room[x-i][y]

        for i in range(object_size_y):
            if y - i >= 0:            
                self.room[x][y-i] = 1
                
            if y + i < len(self.room[x]):
                self.room[x][y+i] = 1


    def check_space(self, object_to_add, x, y, z=0):
        # Check if these coordenates are available in the room
        # Set as 1 the space ocuped by the object

        object_size_x = int(config.POSSIBLE_OBJECTS[object_to_add]['size']['x'] * 10)
        object_size_y = int(config.POSSIBLE_OBJECTS[object_to_add]['size']['y'] * 10)

        if self.room[x][y] == 1:
            return False

        for i in range(object_size_x):
            if x + i < len(self.room):
                if self.room[x+i][y] == 1:
                    return False
                    
            if x - i >= 0:
                if self.room[x-i][y] == 1:
                    return False
                    
        for i in range(object_size_y):
            if y - i >= 0:
                if self.room[x][y-i] == 1:
                    return False

            if y + i < len(self.room[x]):
                if self.room[x][y+i] == 1:
                    return False
        
        return True


    def get_possible_random_possition(self, object_to_add):
        # Return X and Y translation where set the object
        self.room
        free_space = False
        
        while not free_space:
            x = (random.random() * self.n_big) - (self.n_big/2)
            y = (random.random() * self.m_big) - (self.m_big/2)
            z = 0
            free_space = self.check_space(object_to_add, x, y, z)
        self.mark_ocuped_space(object_to_add, x, y)
        
        return x, y, z


    def add_element(self, object_to_add):
        
        x, y, z = self.get_possible_random_possition(object_to_add)
        print(x,y,x)
        self.objects.append({
            'furniture': object_to_add,
            'features': 'translation {x} {z} {y}\n {size} \n\t rotation 0 0 0 0'.format(
                    x=x, y=y, z=z,
                    size=config.POSSIBLE_OBJECTS[object_to_add].get('sizes', '')
                ),
            'name': 'obj{}'.format(self.num_elements)
        })
        self.num_elements += 1


    def add_element_with_translation(self, object_to_add, x, y):
        z = 0

        # Template range map is from -n/2 to n/2 and -m/2 to m/2
        # And world.room is from 0 to n and m * 10
        # So it is necesssary x/10 - n/2 and y/10 - m/2
        
        
        print('En el mapa: ', x/10-self.n/2, y/10-self.m/2)
        self.objects.append({
            'furniture': object_to_add,
            'features': 'translation {x} {z} {y}\n {size} \n\t rotation 0 0 0 0'.format(
                    x=x/10-self.n/2, y=y/10-self.m/2, z=z,
                    size=config.POSSIBLE_OBJECTS[object_to_add].get('sizes', '')
                ),
            'name': 'obj{}'.format(self.num_elements)
        })
        self.mark_ocuped_space(object_to_add, x, y)
        self.num_elements += 1