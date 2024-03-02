import pexpect
import re
import sys
import time
import configs.env

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
#infra_hostname=''

def attach_to_cli_vm_telnet_console(port):
    return attach_to_cli_raw(configs.env.CONSOLE_TEMPLATE.format(configs.env.ENVIRONMENT_IP, port))

def attach_to_cli_raw(command):
    #spawn = pexpect.spawnu(command, timeout=270, encoding='utf-8')
    print('\nService Log Message: Start new pexpect session. Run command "{}"'.format(command))
    spawn = pexpect.spawnu(command, timeout=270)
    spawn.logfile_read = sys.stdout
    return spawn


def linuxchan_grub(name, spawn):
    key = '\x76'  # '\x76' is 'v'
    spawn.send('\x5e')  #http://defindit.com/ascii.html
    spawn.expect('\*[A-Za-z]+ ')
    for i in range(20):
        spawn.send(key)
        # use sleep only for debug purposes
        # if need human readable pause in switch between grub menu
        #time.sleep(1)
        spawn.expect('\*[A-Za-z]+ ')
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


def infra_get_shell(login, password, spawn):
    global infra_hostname
    infra_hostname = login
    spawn.expect('\]\)\?\ ')
    spawn.sendline('yes')
    spawn.expect('assword:')
    spawn.sendline(password)
    spawn.expect('\\{}'.format( endline_char))
    spawn.sendline('PS1="infra@infra:~$"')
    spawn.expect('{}@{}{}$'.format( login, login, eut_operator_promt))
    spawn.sendline('')
    spawn.expect('{}@{}{}$'.format( login, login, eut_operator_promt))



def run_infra_cmd(cmd, spawn):
    #spawn.setecho(False)
    spawn.sendline('')
    spawn.expect('{}@{}{}$'.format( infra_hostname, infra_hostname, eut_operator_promt))
    #spawn.setecho(True)
    spawn.sendline(cmd)
    spawn.expect('{}@{}{}$'.format( infra_hostname, infra_hostname, eut_operator_promt))


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


def eut_operator_send_raw_command(cmd, after_promt, spawn, timeout=10):
    spawn.sendline(cmd)
    spawn.expect(after_promt, timeout=timeout)
