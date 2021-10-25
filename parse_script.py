import os, sys
import argparse
import re
import progressbar
import time

files = []

def draw_progress_file(c, s):
    print("  %d%% \r"%(c/s * 101), file=sys.stderr, end='')

def work_with_file(path, search):
    check_is_file = os.path.isfile(path)
    if check_is_file == True:
        try:
            read_and_write(path, search)
        except PermissionError as err:
            print(f'Permission denied: {err}')


def read_and_write(path, search):
    with open(path, 'r', encoding='utf-8') as input_file:
            with open('out.txt', 'a+', encoding='utf-8') as out_file:
                out_file.seek(0, 2)
                size = os.fstat(input_file.fileno()).st_size
                curPos = 0
                for line in input_file:
                    curPos = curPos + len(line.encode('utf8'))
                    if re.search(f"{search}", line):
                        out_file.write(line)
                    draw_progress_file(curPos, size)
                    time.sleep(0.001)
                out_file.write('\n')



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
    counter = 0
    check_file = os.path.exists(path) #check  is path in arg exists
    if check_file == True:
        print(f'{path} exists')
        if os.path.isfile(path) == True: #if it's a file do search
            print('is file')
            file_name, file_name_res = os.path.splitext(path)
            if re.match('\.log$|\.txt', str(file_name_res)): #other formats are unlikely
                work_with_file(path, search)
        elif os.path.isdir(path) == True: #if it's a dir search for files in dir
            print('is dir')
            try:
                for file_name in os.listdir(path):
                    if re.match('(.*\.+log$)|(.*\.+txt$)', str(file_name)):  #other formats are unlikely
                        files.append(os.path.join(path, file_name))
                bar = progressbar.ProgressBar(maxval=len(files)+1).start()
                bar_ind = 1
                bar.update(bar_ind)
                for file_name in files:
                    print(file_name,"\n")
                    work_with_file(file_name, search)
                    counter += 1
                    print(counter)
                    bar_ind = bar_ind + 1
                    bar.update(bar_ind)
                bar.finish()
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