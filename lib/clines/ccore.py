import pexpect
import sys
import re
import os
import requests
import json
from .chars import *


eut_login = 'vyos'
eut_password = 'vyos'
eut_hostname = 'vyos'
eut_login_promt = 'login: ' + endline_char
eut_password_promt = 'Password: ' + endline_char
eut_operator_promt = ":\~\\" + endline_char
eut_admin_promt = (
    eut_login +
    '@' +
    eut_hostname +
    '#'
)
eut_for_login_promt = (
    eut_login_promt +
    pipe_char +
    eut_password_promt +
    pipe_char +
    eut_operator_promt +
    pipe_char
    + eut_admin_promt
)
eut_exit_cmd = 'exit'
eut_log_file = 'sys.stdout'


def start_vm(vm):
    os.system('virsh start ' + vm)


def destroy_vm(vm):
    os.system('virsh destroy ' + vm)


def shutdown_vm(vm):
    os.system('virsh shutdown ' + vm)


def init_bridge_interface(bridge):
    os.system('ip link add name ' + bridge + ' type bridge')
    os.system('ip link set dev ' + bridge + ' up')


def create_dir(path):
    dir_name = os.path.dirname(path)
    if dir_name != empty_char:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        return True
    return False


def create_file(log_file):
    create_dir(log_file)
    return open(log_file, 'w')


def attach_to_cli(command):
    spawn = pexpect.spawnu(command, timeout=270)
    if create_dir(eut_log_file):
        spawn.logfile = create_file(eut_log_file)
    else:
        spawn.logfile = eut_log_file
    return spawn


def print_all(spawn):
    print('#####before:')
    print(spawn.before)
    print('#####after:')
    print(spawn.after)
    print('#####:')

def dut_get_operator(login, password, hostname, spawn):
    spawn.sendline(empty_char)
    spawn.expect(eut_for_login_promt)
    if re.search(eut_operator_promt, spawn.after):
        True
    elif re.search(eut_login_promt, spawn.after):
        spawn.sendline(login)
        spawn.expect(eut_password_promt)
        spawn.sendline(password)
        spawn.expect(eut_operator_promt)
    elif re.search(eut_admin_promt, spawn.after):
        spawn.sendline(eut_exit_cmd)
        spawn.expect(eut_operator_promt)


def dut_get_admin(login, password, hostname, spawn):
    spawn.sendline(empty_char)
    spawn.expect(eut_for_login_promt)
    if re.search(eut_admin_promt, spawn.after):
        True
    elif re.search(eut_login_promt, spawn.after):
        dut_get_operator(login, password, hostname, spawn)
        dut_from_operator_to_admin(spawn)
    elif re.search(eut_operator_promt, spawn.after):
        dut_from_operator_to_admin(spawn)


def dut_from_operator_to_admin(spawn):
        spawn.sendline('configure')
        spawn.expect(eut_admin_promt)


def dut_operator_sudo(cmd, spawn):
    spawn.sendline('sudo ' + cmd)
    spawn.expect(eut_operator_promt)


def dut_operator_send_raw_command(cmd, promt, spawn):
    spawn.sendline(cmd)
    spawn.expect(promt)
