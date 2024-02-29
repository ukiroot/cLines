from .vm_virsh import \
    destroy_vm, add_interface_to_bridge

def destroy_topology(euts, linuxchans):
    for eut in euts:
        destroy_vm(eut)
    for linuxchan in linuxchans:
        destroy_vm(linuxchan)


def init_topology(topology):
    for dict_of_interfaces in topology.values():
        for vnet_intefrace, bridge in dict_of_interfaces.items():
            add_interface_to_bridge(vnet_intefrace, bridge)