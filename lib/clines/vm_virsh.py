import json
import re
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "./"))
import pool

def system(cmd):
    pool.resapi_request(
        'POST',
        '{}{}'.format(pool.rest_service_url, '/cmd_by_http'),
        {"cmd": cmd}, pool.content_type_header
    )


def get_vm_interfaces_request(vm_name):
    response = pool.resapi_request(
        'POST',
        '{}{}'.format(pool.rest_service_url, '/get_vm_interfaces'),
        {"vm": vm_name}, pool.content_type_header
    )
    return json.loads(response.text)['interfaces']


def start_vm(vm):
    system('sudo virsh start ' + vm)


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

