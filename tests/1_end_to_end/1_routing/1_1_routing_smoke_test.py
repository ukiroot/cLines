import pytest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
import lib.clines as clines
import configs.env


@pytest.fixture(autouse=True)
def init():
    # Init step 0. Reserve resources
    global \
        linuxchan0_spawn,\
        linuxchan1_spawn, \
        eut0_spawn, \
        eut1_spawn, \
        eut_names, \
        linuxchan_names

    # Init step 1. Reserve resources
    eut_names = clines.get_euts(2)
    linuxchan_names = clines.get_linuxchans(2)
    bridges = clines.get_bridges(3)

    # Init step 2. Resolve reserved resources names
    eut0=eval('configs.env.{}'.format(eut_names[0]))
    eut1=eval('configs.env.{}'.format(eut_names[1]))
    linuxchans0=eval('configs.env.{}'.format(linuxchan_names[0]))
    linuxchans1=eval('configs.env.{}'.format(linuxchan_names[1]))

    # Init Step 3: start EUT VMs.
    clines.start_vm(eut_names[0])
    clines.start_vm(eut_names[1])
    eut0_spawn = clines.attach_to_cli_vm_telnet_console(eut0.get("console_port"))
    eut1_spawn = clines.attach_to_cli_vm_telnet_console(eut1.get("console_port"))
    clines.eut_wait_login_promt(eut0_spawn)
    clines.eut_wait_login_promt(eut1_spawn)

    # Init Step 4: start linuxchans VMs. Hostname for linuxchans configure via grub menu, so after start
    # immediately connect to VMs and init pexpect spawn
    clines.start_vm(linuxchan_names[0])
    linuxchan0_spawn = clines.attach_to_cli_vm_telnet_console(linuxchans0.get("console_port"))
    clines.linuxchan_grub(linuxchan_names[0], linuxchan0_spawn)
    clines.start_vm(linuxchan_names[1])
    linuxchan1_spawn = clines.attach_to_cli_vm_telnet_console(linuxchans1.get("console_port"))
    clines.linuxchan_grub(linuxchan_names[1], linuxchan1_spawn)

    # Init Step 5: Resolve VMs interfaces.
    eut0 = clines.get_vm_interfaces(eut_names[0])
    eut1 = clines.get_vm_interfaces(eut_names[1])
    linuxchans0 = clines.get_vm_interfaces(linuxchan_names[0])
    linuxchans1 = clines.get_vm_interfaces(linuxchan_names[1])

    # Init Step 6: Create bridges interfaces.
    clines.init_bridge_interface(bridges[0])
    clines.init_bridge_interface(bridges[1])
    clines.init_bridge_interface(bridges[2])

    # Init Step 7: Determine network topology for VMs.
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

    # Init Step 8: Init topology. Add VMs interfaces to bridges
    clines.init_topology(dict(topology_euts, **topology_linuxchans))

    # Run test
    yield

    # Finalize Step 0: Turn off VMs
    clines.destroy_topology(eut_names, linuxchan_names)
    # Finalize Step 1: Return reserved resources
    clines.release_euts(eut_names)
    clines.release_bridges(bridges)
    clines.release_linuxchans(linuxchan_names)


@pytest.mark.end_to_end_routing_smoke
def test_routing_smoke():
    clines.information_log('Configuration client: {}'.format(linuxchan_names[0]))
    clines.linuxchan_get_shell(linuxchan_names[0], linuxchan0_spawn)
    clines.linuxchan_set_ip('eth0', '10.0.0.2/24', linuxchan0_spawn)
    clines.linuxchan_default_gw ('10.0.0.1', linuxchan0_spawn)

    clines.information_log('Configuration client: {}'.format(linuxchan_names[1]))
    clines.linuxchan_get_shell(linuxchan_names[1], linuxchan1_spawn)
    clines.linuxchan_set_ip('eth0', '10.0.1.2/24', linuxchan1_spawn)
    clines.linuxchan_default_gw ('10.0.1.1', linuxchan1_spawn)

    clines.information_log('Configuration EUT: {}'.format(eut_names[0]))
    clines.eut_admin_send_raw_command('set interfaces ethernet eth0 address 192.0.1.1/30', eut0_spawn)
    clines.eut_admin_send_raw_command('set interfaces ethernet eth1 address 10.0.0.1/24', eut0_spawn)
    clines.eut_admin_send_raw_command('set protocols static route 10.0.1.0/24 next-hop 192.0.1.2', eut0_spawn)
    clines.eut_admin_send_raw_command('commit', eut0_spawn)

    clines.information_log('Configuration EUT: {}'.format(eut_names[1]))
    clines.eut_admin_send_raw_command('set interfaces ethernet eth0 address 192.0.1.2/30', eut1_spawn)
    clines.eut_admin_send_raw_command('set interfaces ethernet eth1 address 10.0.1.1/24', eut1_spawn)
    clines.eut_admin_send_raw_command('set protocols static route 10.0.0.0/24 next-hop 192.0.1.1', eut1_spawn)
    clines.eut_admin_send_raw_command('commit', eut1_spawn)

    clines.information_log('End to end tests start:')
    clines.information_log('Ping from {} to {}'.format(linuxchan_names[0], linuxchan_names[1]))
    clines.linuxchan_ping( '10.0.1.2', linuxchan0_spawn)
    clines.information_log('Ping from {} to {}'.format(linuxchan_names[1], linuxchan_names[0]))
    clines.linuxchan_ping( '10.0.0.2', linuxchan1_spawn)
