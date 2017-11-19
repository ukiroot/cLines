import pexpect
import sys
import re
import os
import requests
import json

empty_char = ''
space_char = ' '
slash_char = '/'
pipe_char = '|'
endline_char = '$'
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
pool_url = 'http://127.0.0.1:5000/restapi/v1.0/pool/'
pool_url_eut = pool_url + 'eut'
pool_url_bridge = pool_url + 'bridge'
pool_url_linuxchan = pool_url + 'linuxchan'


def start_vm(vm):
    os.system('virsh start ' + vm)


def destroy_vm(vm):
    os.system('virsh destroy ' + vm)


def shutdown_vm(vm):
    os.system('virsh shutdown ' + vm)


def create_dir(path):
    dir_name = os.path.dirname(path)
    if dir_name != empty_char:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        return True
    return False


def attach_to_cli(command):
    spawn = pexpect.spawnu(command, timeout=270)
    if create_dir(eut_log_file):
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


def resapi_request(method, uri, body='', headers='', debug=False):
    method = method.upper()
    data = json.dumps(body)
    if method == 'PUT':
        response = requests.put(uri, data, headers=headers)
    elif method == 'POST':
        response = requests.post(uri, data, headers=headers)
    elif method == 'GET':
        response = requests.get(uri, headers=headers)
    elif method == 'DELETE':
        response = requests.delete(uri, headers=headers)
    else:
        print(method + " is wrong HTTP method or not implemented in func")
        return False
    if debug is True:
        print("Status_code:")
        print(response.status_code)
        print("Response_body:")
        print(response.text)
    return response


def add_resource(uri, body):
    resapi_request('POST', uri, body, {"Content-Type": "application/json"})


def add_eut(body):
    add_resource(pool_url_eut, body)


def get_resource_body(name, settings):
    body = {
                'name': name,
                'settings': [settings]
            }
    return body
