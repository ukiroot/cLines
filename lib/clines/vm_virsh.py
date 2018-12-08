import os
import subprocess
import re


def start_vm(vm):
    os.system('sudo virsh start ' + vm)


def destroy_vm(vm):
    os.system('sudo virsh destroy ' + vm)


def shutdown_vm(vm):
    os.system('sudo virsh shutdown ' + vm)


def init_bridge_interface(bridge):
    os.system('sudo ip link add name ' + bridge + ' type bridge')
    os.system('sudo ip link set dev ' + bridge + ' up')


def add_interface_to_bridge(interface, bridge):
    os.system('sudo ip del ' + bridge)
    os.system('sudo ip link set ' + interface + ' master ' + bridge)


def get_vm_interface(vm):
    return re.findall(
        ('vnet[0-9]+'),
        subprocess.check_output(
            'sudo virsh domiflist ' +
            vm +
            "| grep vnet | awk '{print $1}'",
            shell=True
        ).decode("utf-8", "strict")
    )
