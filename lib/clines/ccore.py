import pexpect
import re
import os
import sys
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


def create_dir(path):
    dir_name = os.path.dirname(path)
    if dir_name != empty_char:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        return True
    return False


def create_file(log_file):
    create_dir(log_file)
    return open(log_file, 'w')


def attach_to_cli(command, log_file=sys.stdout):
    spawn = pexpect.spawnu(command, timeout=270)
    if create_dir(log_file):
        spawn.logfile = create_file(log_file)
    return spawn


def linuxchan_grub(name, spawn):
    key = '\x76'  # '\x76' is 'v'
    spawn.send('')
    spawn.expect('\*[A-Za-z]+')
    for i in range(100):
        spawn.send(key)
        spawn.expect('\*[A-Za-z]+')
        if name in spawn.after:
            break
        if i == 99:
            raise Exception("Pattern didn't find in Grub menu")
    spawn.sendline('')
    spawn.expect('[a-z]+' + ' login:')
    if name + ' login:' not in spawn.after:
        raise Exception(
            """After boot expetc promt:
             {0}
             but promt was:
             {1}
             """.format(name + ' login:', spawn.after)
        )


def linuxchan_get_shell(name, spawn):
    spawn.sendline('')
    spawn.expect(name + " login:")
    spawn.sendline('root')
    spawn.expect("Password:")
    spawn.sendline('admin')
    spawn.expect("root@" + name + r':~#')


def print_all(spawn):
    print('#####before:')
    print(spawn.before)
    print('#####after:')
    print(spawn.after)
    print('#####:')


def eut_get_operator(login, password, hostname, spawn):
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


def eut_get_admin(login, password, hostname, spawn):
    spawn.sendline(empty_char)
    spawn.expect(eut_for_login_promt)
    if re.search(eut_admin_promt, spawn.after):
        True
    elif re.search(eut_login_promt, spawn.after):
        eut_get_operator(login, password, hostname, spawn)
        eut_from_operator_to_admin(spawn)
    elif re.search(eut_operator_promt, spawn.after):
        eut_from_operator_to_admin(spawn)


def eut_from_operator_to_admin(spawn):
        spawn.sendline('configure')
        spawn.expect(eut_admin_promt)


def eut_operator_sudo(cmd, spawn):
    spawn.sendline('sudo ' + cmd)
    spawn.expect(eut_operator_promt)


def eut_operator_send_raw_command(cmd, promt, spawn):
    spawn.sendline(cmd)
    spawn.expect(promt)
