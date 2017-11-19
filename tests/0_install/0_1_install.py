import sys
import os


def test():
    euts.start_vm(vm_name)
    eut_1_spawn = euts.attach_to_cli(vm_console)
    euts.dut_get_operator(
        euts.eut_login,
        euts.eut_password,
        euts.eut_hostname,
        eut_1_spawn
    )
    install_promts = (
        '\]:|\]Mb:|\]MB:|' +
        euts.eut_login +
        "':"
    )
    list_of_input_commands = [
        'install system',
        'Yes',
        'Auto',
        'sda',
        'Yes',
        '',
        '',
        euts.eut_password,
        euts.eut_password
    ]
    for command in list_of_input_commands:
        euts.dut_operator_send_raw_command(
            command,
            install_promts,
            eut_1_spawn
        )
    euts.dut_operator_send_raw_command(
        'sda',
        euts.eut_operator_promt,
        eut_1_spawn
    )

    euts.add_eut(euts.get_resource_body(vm_name, vm_console))
    euts.destroy_vm(vm_name)


if __name__ == '__main__':
    sys.path.append(
        os.path.abspath(os.path.dirname(sys.argv[0])) +
        '/../../lib'
    )
    import euts
    test_args_values = sys.argv[3].split(', ')
    test_args_names = sys.argv[2].split(', ')
    euts.eut_log_file = sys.argv[1]
    vm_name = test_args_values[0]
    vm_console = test_args_values[1]
    test()
