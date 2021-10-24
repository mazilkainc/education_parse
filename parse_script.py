import os, sys
import argparse
import re

#hardcoded word
mask = 'Error'
files = []

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

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', nargs='+', default=[''], help='path to file or path to dir')
    return parser


def check_file(path):
    check_file = os.path.exists(path) #check  is path in arg exists
    if check_file == True:
        print(f'{path} exists')
        if os.path.isfile(path) == True: #if it's a file do search
            print('is file')
            file_name, file_name_res = os.path.splitext(path)
            if re.match('\.log$|\.txt', str(file_name_res)): #other formats are unlikely
                work_with_file(path)
        elif os.path.isdir(path) == True: #if it's a dir search for files in dir
            print('is dir')
            try:
                for file_name in os.listdir(path):
                    if re.match('(\w+\.+log$)|(\w+\.+txt$)', str(file_name)):  #other formats are unlikely
                        files.append(os.path.join(path, file_name))
                try:
                    for file_name in files:
                        work_with_file(file_name)
                except FileNotFoundError as e:
                    print(e)
            except PermissionError as err:
                print(f'Permission denied: {err}')
    else:
        print(f'check the path in arg')

parser = createParser()
namespace = parser.parse_args(sys.argv[1:])

for name in namespace.path:
    check_file(name)