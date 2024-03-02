import pytest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
import lib.clines as clines
import configs.env


@pytest.fixture(autouse=True)
def init():
    global \
        linuxchan0_spawn,\
        linuxchan1_spawn, \
        eut0_spawn, \
        eut1_spawn, \
        eut_names, \
        linuxchan_names

    eut_names = clines.get_euts(2)
    linuxchan_names = clines.get_linuxchans(2)
    bridges = clines.get_bridges(3)
    eut0=eval('configs.env.{}'.format(eut_names[0]))
    eut1=eval('configs.env.{}'.format(eut_names[1]))
    linuxchans0=eval('configs.env.{}'.format(linuxchan_names[0]))
    linuxchans1=eval('configs.env.{}'.format(linuxchan_names[1]))

    clines.start_vm(eut_names[0])
    clines.start_vm(eut_names[1])

    clines.start_vm(linuxchan_names[0])
    linuxchan0_spawn = clines.attach_to_cli_vm_telnet_console(linuxchans0.get("console_port"))
    clines.linuxchan_grub(linuxchan_names[0], linuxchan0_spawn)

    clines.start_vm(linuxchan_names[1])
    linuxchan1_spawn = clines.attach_to_cli_vm_telnet_console(linuxchans1.get("console_port"))
    clines.linuxchan_grub(linuxchan_names[1], linuxchan1_spawn)

    eut0 = clines.get_vm_interfaces(eut_names[0])
    eut1 = clines.get_vm_interfaces(eut_names[1])
    linuxchans0 = clines.get_vm_interfaces(linuxchan_names[0])
    linuxchans1 = clines.get_vm_interfaces(linuxchan_names[1])

    clines.init_bridge_interface(bridges[0])
    clines.init_bridge_interface(bridges[1])
    clines.init_bridge_interface(bridges[2])

    topology_euts = {
        eut_names[0]: {
            eut0[0]: bridges[0],
            eut0[1]: bridges[1],
            eut0[2]: bridges[1],
            eut0[3]: bridges[1],
        },
        eut_names[1]: {
            eut1[0]: bridges[0],
            eut1[1]: bridges[2],
            eut1[2]: bridges[2],
            eut1[3]: bridges[2],
        }
    }
    topology_linuxchans = {
        linuxchan_names[0]: {
            linuxchans0[0]: bridges[1]
        },
        linuxchan_names[1]: {
            linuxchans1[0]: bridges[2]
        }
    }

    clines.init_topology(dict(topology_euts, **topology_linuxchans))
    yield
    clines.destroy_topology(eut_names, linuxchan_names)
    clines.release_euts(eut_names)
    clines.release_bridges(bridges)
    clines.release_linuxchans(linuxchan_names)


@pytest.mark.end_to_end_routing_smoke
def test_routing_smoke():
    clines.linuxchan_get_shell(linuxchan_names[0], linuxchan0_spawn)
    clines.linuxchan_get_shell(linuxchan_names[1], linuxchan1_spawn)