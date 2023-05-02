
import subprocess
import pathlib
import os
import sys


ST_FREQUENСY        = 4000
ST_LOAD_TYPE        = 'SWD'
ST_LINK_CLI_PATH    = 'C:\Program Files (x86)\STMicroelectronics\STM32 ST-LINK Utility\ST-LINK Utility\ST-LINK_CLI.exe'
ST_FIRMWARE_PATH    = ''
ST_LOAD_ADDR        = 0x08000000

ST_HEAD_CMD_PREFIX  = '\"' + ST_LINK_CLI_PATH + '\"' + ' -c ' + ST_LOAD_TYPE  + ' Freq=' + str(ST_FREQUENСY)

POSSIBLE_BINARY_DIRS    = [
    './Build/', 
    './build/', 
    './Debug/', 
    './debug/'
]

BINARY_FILE_EXTENSIONS  = [
    '.bin', 
    '.hex'
]

class ExecCmd:
    def __init__(self, exec_name, exec_string):
        self.name   = exec_name
        self.cmd    = exec_string


def find_binary_in_possible_dirs():
    for dir in POSSIBLE_BINARY_DIRS:
        for ref in BINARY_FILE_EXTENSIONS:
            files = list(map(str, pathlib.Path(dir).glob('*' + ref)))
            if files:
                return files[0]
        
    return None

def get_output_width(commands_list):
    name_list = [i.name for i in commands_list]
    return max(map(len, name_list))


if __name__ == '__main__':

    if len(ST_FIRMWARE_PATH) == 0:
        if len(sys.argv) < 2:
            ST_FIRMWARE_PATH = find_binary_in_possible_dirs()
            if not ST_FIRMWARE_PATH:
                print("error: can not find binary file")
                exit(1)
            else:
                print("binary found:", ST_FIRMWARE_PATH)
        else:
            ST_FIRMWARE_PATH = sys.argv[1]

    exec_cmd_list = [
        ExecCmd("chip erase",   ST_HEAD_CMD_PREFIX + ' -ME'),
        ExecCmd("load binary",  ST_HEAD_CMD_PREFIX + ' -P ' + ST_FIRMWARE_PATH + ' ' + hex(ST_LOAD_ADDR)),
        ExecCmd("reset mk",     ST_HEAD_CMD_PREFIX + ' -Rst')
    ]

    exec_name_width = get_output_width(exec_cmd_list)

    print("burning start:")
    for cmd in exec_cmd_list:
        name = '(\"' + cmd.name + '\")'
        print("run %s cmd\t:" % name.ljust(exec_name_width + 4), end='')
        result = subprocess.run(cmd.cmd, shell=True, capture_output=True)
        if result.returncode != 0:
            print('\b\t[error]')
            print("proccess output:")
            print("-------------------------------")
            print(result.stdout.decode(), end='')
            print("-------------------------------")
            exit(1)
        else:
            print('\b\t[success]')

    exit(0)
            