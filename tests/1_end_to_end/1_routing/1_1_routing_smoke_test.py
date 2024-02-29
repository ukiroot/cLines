import sys
import os
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import lib.clines as clines

@pytest.fixture(autouse=True)
def init():
    euts = clines.get_euts(2)
    linuxchans = clines.get_linuxchans(2)
    bridges = clines.get_bridges(3)

    clines.start_vm(euts[0])
    clines.start_vm(euts[1])
    clines.start_vm(linuxchans[0])
    clines.start_vm(linuxchans[1])

    eut0 = clines.get_vm_interfaces(euts[0])
    eut1 = clines.get_vm_interfaces(euts[1])
    linuxchans0 = clines.get_vm_interfaces(linuxchans[0])
    linuxchans1 = clines.get_vm_interfaces(linuxchans[1])

    clines.init_bridge_interface(bridges[0])
    clines.init_bridge_interface(bridges[1])
    clines.init_bridge_interface(bridges[2])

    topology_euts = {
        euts[0]: {
            eut0[0]: bridges[0],
            eut0[1]: bridges[1],
            eut0[2]: bridges[1],
            eut0[3]: bridges[1],
        },
        euts[1]: {
            eut1[0]: bridges[0],
            eut1[1]: bridges[2],
            eut1[2]: bridges[2],
            eut1[3]: bridges[2],
        }
    }
    topology_linuxchans = {
        linuxchans[0]: {
            linuxchans0[0]: bridges[1]
        },
        linuxchans[1]: {
            linuxchans1[0]: bridges[2]
        }
    }

    clines.init_topology(dict(topology_euts, **topology_linuxchans))
    yield
    clines.destroy_topology(euts, linuxchans)
    clines.release_euts(euts)
    clines.release_bridges(bridges)
    clines.release_linuxchans(linuxchans)


@pytest.mark.end_to_end_routing_smoke
def test_routing_smoke():
    True
