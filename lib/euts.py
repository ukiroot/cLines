import pexpect
import sys
import re
import os

empty_char = ''
space_char = ' '
slash_char = '/'
eut_login = 'vyos'
eut_password = 'vyos'
eut_hostname = 'vyos'
eut_login_promt = 'login: $'
eut_password_promt = 'Password: $'
eut_operator_promt = ':\~\$'
eut_admin_promt = (
    eut_login +
    '@' +
    eut_hostname +
    '#'
)
eut_for_login_promt = (
    eut_login_promt +
    '|' +
    eut_password_promt +
    '|' +
    eut_operator_promt +
    '|'
    + eut_admin_promt
)
eut_exit_cmd = 'exit'
eut_log_file = 'sys.stdout'
eut_console = {'EUT_1': 'telnet 127.0.0.1 7001',
               'EUT_2': 'telnet 127.0.0.1 7002',
               'EUT_3': 'telnet 127.0.0.1 7003',
               'EUT_4': 'telnet 127.0.0.1 7004',
               'EUT_5': 'telnet 127.0.0.1 7005',
               'EUT_6': 'telnet 127.0.0.1 7006',
               'EUT_7': 'telnet 127.0.0.1 7007',
               'EUT_8': 'telnet 127.0.0.1 7008'}


def start_vm(vm):
    os.system('virsh start ' + vm)


def destroy_vm(vm):
    os.system('virsh destroy ' + vm)


def shutdown_vm(vm):
    os.system('virsh shutdown ' + vm)


def attach_to_cli(command):
    spawn = pexpect.spawnu(command, timeout=270)
    log_dir_name = os.path.dirname(eut_log_file)
    if log_dir_name != empty_char:
        if not os.path.exists(log_dir_name):
            os.makedirs(log_dir_name)
        desc_of_log_file = open(eut_log_file, 'w')
        spawn.logfile = desc_of_log_file
    else:
        spawn.logfile = eut_log_file
    return spawn


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
#    print_all(spawn)


def print_all(spawn):
    print('#####before:')
    print(spawn.before)
    print('#####after:')
    print(spawn.after)
    print('#####:')
