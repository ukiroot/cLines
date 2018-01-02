import re
from .vm_virsh import \
    get_vm_interface, \
    add_interface_to_bridge


def update_br(brs_resource, topology):
    count = 0
    for br_conf in brs_resource:
        fixed_topology = re.sub('br' + str(count), br_conf['name'], topology)
        count = count + 1
    return fixed_topology


def update_eth(vm_interfaces, node_topology):
    count = 0
    fix_topology = node_topology
    for vm_interface in vm_interfaces:
        fix_topology = re.sub('eth' + str(count), vm_interface, fix_topology)
        count = count + 1
    return fix_topology


def init_topology(euts, linuxchans, brs_resource, topology):
    node_names = []
    topology = update_br(brs_resource, topology)
    topology_of_node = topology.split("|")
    count = 0
    for eut in euts:
        node_names.append(eut['name'])
    for linuxchan in linuxchans:
        node_names.append(linuxchan['name'])

    for node in topology_of_node:
        vm_interfaces = get_vm_interface(node_names[count])
        topology_of_interface = update_eth(vm_interfaces, node).split(",")
        for interface in topology_of_interface:
            interface_name = interface.split(":")[0]
            bridge_name = interface.split(":")[1]
            add_interface_to_bridge(interface_name, bridge_name)
        count = count + 1
