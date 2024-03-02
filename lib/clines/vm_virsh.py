import re
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "./"))
from ccore import infra_get_shell, attach_to_cli, run_infra_cmd
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import configs.env

infra_spawn = attach_to_cli('ssh {}@{}'.format(configs.env.ENVIRONMENT_LOGIN, configs.env.ENVIRONMENT_IP))
infra_get_shell(configs.env.ENVIRONMENT_LOGIN, configs.env.ENVIRONMENT_PASSOWORD, infra_spawn)

def system(cmd):
    run_infra_cmd(cmd, infra_spawn)


def get_vm_interfaces_request(vm):
    cmd = '{} {} {}'.format('sudo virsh domiflist ', vm, "| grep vnet | awk '{print $1}'| xargs echo ")
    system(cmd)
    return infra_spawn.before.split("\x1b[?2004l\r")[1].split("\x1b[?2004h")[0]


def start_vm(vm):
    system('sudo virsh start {}'.format(vm))


def reset_vm(vm):
    system('sudo virsh reset {}'.format(vm))


def destroy_vm(vm):
    system('sudo virsh destroy ' + vm)


def shutdown_vm(vm):
    system('sudo virsh shutdown ' + vm)


def init_bridge_interface(bridge):
    system('sudo ip link del ' + bridge)
    system('sudo ip link add name ' + bridge + ' type bridge')
    system('sudo ip link set dev ' + bridge + ' up')


def add_interface_to_bridge(interface, bridge):
    system('sudo ip link set ' + interface + ' master ' + bridge)


def get_vm_interfaces(vm):
    return re.findall(
        ('vnet[0-9]+'),
        get_vm_interfaces_request(vm)
    )