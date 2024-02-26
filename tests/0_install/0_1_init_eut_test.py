import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import lib.clines as clines
import configs.env


def install_vyos_from_iso_to_disk(eut):
    eut_name = eut.get('name')
    eut_console = configs.env.CONSOLE_TEMPLATE.format(configs.env.ENVIRONMENT_IP, eut.get("console_port"))

    clines.destroy_vm(eut_name)
    clines.start_vm(eut_name)
    eut_1_spawn = clines.attach_to_cli(eut_console)
    clines.eut_get_operator(
        clines.eut_login,
        clines.eut_password,
        clines.eut_hostname,
        eut_1_spawn
    )
    install_promts = (
        'y/N\]|' +
        '[0-9]\)|' +
        'vyos\)|' +
        ': K\)|' +
        '/dev/sda\)|' +
        'Y/n\]|' +
        clines.eut_login +
        "':"
    )
    list_of_input_commands = [
        'install image',  # In version VyOS 1.1 was 'install system'
        'Yes',            # Would you like to continue? [y/N] Yes
        '',               # What would you like to name this image? (Default: 1.5-rolling-202402240021)
        '',               # Please enter a password for the "vyos" user (Default: vyos)
        'S',              # What console should be used by default? (K: KVM, S: Serial, U: USB-Serial)? (Default: K)
        '',               # Which one should be used for installation? (Default: /dev/sda)
        'Y',              # Installation will delete all data on the drive. Continue? [y/N]

    ]
    for command in list_of_input_commands:
        clines.eut_operator_send_raw_command(
            command,
            install_promts,
            eut_1_spawn
        )

    clines.eut_operator_send_raw_command(
         'Y',             # Would you like to use all the free space on the drive? [Y/n]
        clines.eut_operator_promt,
        eut_1_spawn
    )

    clines.add_eut(clines.get_resource_body(eut_name, eut_console))
    clines.destroy_vm(eut_name)


def test_install_eut_1():
    install_vyos_from_iso_to_disk(configs.env.EUT_1)
