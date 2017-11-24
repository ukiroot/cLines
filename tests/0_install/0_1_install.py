import sys
import os


def test(eut_name, eut_console):
    core.start_vm(eut_name)
    eut_1_spawn = core.attach_to_cli(eut_console)
    core.dut_get_operator(
        core.eut_login,
        core.eut_password,
        core.eut_hostname,
        eut_1_spawn
    )
    install_promts = (
        '\]:|\]Mb:|\]MB:|' +
        core.eut_login +
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
        core.eut_password,
        core.eut_password
    ]
    for command in list_of_input_commands:
        core.dut_operator_send_raw_command(
            command,
            install_promts,
            eut_1_spawn
        )
    core.dut_operator_send_raw_command(
        'sda',
        core.eut_operator_promt,
        eut_1_spawn
    )

    add_eut(get_resource_body(eut_name, eut_console))
    core.destroy_vm(eut_name)


if __name__ == '__main__':
    sys.path.append(
        os.path.abspath(os.path.dirname(sys.argv[0])) +
        '/../../lib'
    )
    from clines import *
    import clines.ccore as core

    args = parse_test_args(sys.argv[1:])
    core.eut_log_file = args.log
    eut_name = args.eut_name
    eut_console = args.eut_console
    test_summary = args.test_summary
    weight = args.weight
    test(eut_name, eut_console)
