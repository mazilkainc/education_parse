import os, sys
import argparse
import re
import progressbar
import time

files = []

def work_with_file(path, search):
    check_is_file = os.path.isfile(path)
    if check_is_file == True:
        try:
            read_and_write(path, search)
        except PermissionError as err:
            print(f'Permission denied: {err}')


def read_and_write(path, search):
    with open(path, 'r', encoding='utf-8') as input_file:
        if os.path.exists(os.getcwd().join('out.txt')) == True:
            with open('out.txt', 'a', encoding='utf-8') as out_file: #if the output file exists, add new lines (for searching in several files)
                for line in input_file:
                    if re.findall(f"{search}", line):
                        out_file.write(line)

        elif os.path.exists(os.getcwd().join('out.txt')) == False:  #if the output file does not exist - creates it, (to read multiple files in the folder)
            with open('out.txt', 'w', encoding='utf-8') as out_file:
                for line in input_file:
                    if re.findall(f"{search}", line):
                        out_file.write(line)


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', nargs='+', default=[''], help='path to file or path to dir')
    parser.add_argument('-s', '--search', nargs='+', default=['[E|e]rror'], type=str, help='use "?" as one character or "*" as several')
    return parser

def mask(search):
    search = search.replace("?", ".")
    search = search.replace("*", "\w+")
    return search

def check_file(path, search):
    check_file = os.path.exists(path) #check  is path in arg exists
    if check_file == True:
        print(f'{path} exists')
        if os.path.isfile(path) == True: #if it's a file do search
            print('is file')
            file_name, file_name_res = os.path.splitext(path)
            if re.match('\.log$|\.txt', str(file_name_res)): #other formats are unlikely
                file_bar = progressbar.ProgressBar(maxval=os.path.getsize(path)).start()
                work_with_file(path, search)
                file_bar.finish()
        elif os.path.isdir(path) == True: #if it's a dir search for files in dir
            print('is dir')
            try:
                for file_name in os.listdir(path):
                    if re.match('(\w+\.+log$)|(\w+\.+txt$)', str(file_name)):  #other formats are unlikely
                        files.append(os.path.join(path, file_name))
                try:
                    bar = progressbar.ProgressBar(maxval=len(files)).start()
                    bar_ind = 1
                    for file_name in files:
                        work_with_file(file_name, search)
                        bar.update(bar_ind)
                        bar_ind = bar_ind + 1
                    bar.finish()
                except FileNotFoundError as e:
                    print(e)
            except PermissionError as err:
                print(f'Permission denied: {err}')
    else:
        print(f'check the path in arg')

parser = createParser()
namespace = parser.parse_args(sys.argv[1:])

for name in namespace.path:
    for search in namespace.search:
        search = mask(search)
        check_file(name, search)