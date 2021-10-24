import os

#The simplest case: read the hardcoded file, search for the hardcoded word, print result to console
path = 'D:/test_py/log.log'
mask = 'Error'

def work_with_file(path):
    check_is_file = os.path.isfile(path)
    if check_is_file == True:
        try:
            read_and_write(path)
        except PermissionError as err:
            print(f'Permission denied: {err}')

def read_and_write(path):
    with open(path, 'r', encoding='utf-8') as input_file:
        for line in input_file:
            if mask in line:
                print(line)

read_and_write(path)
