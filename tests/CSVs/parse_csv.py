import csv
import os


from glob import glob

import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-d', '--directory', type=str, default='3', required=False, help='Folder where get csvs to parse')
args = ap.parse_args()

all_rows = []

for result in glob('{}/*.csv'.format(args.directory)):
    print(result)
    num_objects = None
    room_size = None
    function = False
    obj = False
    size = False
    
    if result.split('\\')[-1] == 'test_all_random.csv':
        header = 'Funciones'
    else:
        type_result = result.split('/')[-1].split('-')[1].split('.')[0]
        header = 'Objetos' if type_result == '10x10' else 'Tamaño'
        if header == 'Objetos':
            room_size = type_result
        else:
            num_objects = int(type_result.split('_')[0])
        
    all_rows.append(result.replace('.csv', ''))
    all_rows.append('{type_r};Ejemplos; ;{type_r};Media'.format(type_r=header))
    with open(result, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate(reader):
            line = ''
            if not row:
                continue

            if (num_objects is None and room_size is None) or function:
                room_size = row[0].split(':')[-1]
                function = True

            else:
                if num_objects is None or obj:
                    print(row)
                    num_objects = int(row[0].split(':')[-1])
                    print(num_objects)
                    obj = True
                
                if room_size is None or size:
                    room_size = row[0].split(':')[-1]
                    size = True
                
            num_examples = row[1].split(':')[-1]
            
            total = 0
            examples = 0
            avg = 0
            for value in row:
                try:
                    v = float(value)
                    total += v
                    examples += 1
                except ValueError:
                    pass
            
            if examples:
                avg = total/examples
                #line += str(total/examples)

            line = '{type_r};{examples};#;{type_r};{avg}'.format(
                type_r = num_objects if header == 'Objetos' else room_size,
                examples=num_examples,
                avg=str(avg).replace('.', ',')
            )
            all_rows.append(line)

with open('{}/all_test.txt'.format(args.directory), 'w') as f:
    for l in all_rows:
        f.write(l)
        f.write('\n')
    
            
