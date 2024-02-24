import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import lib.clines as clines


def test(eut_name, eut_console, log_file):
    clines.start_vm(eut_name)
    eut_1_spawn = clines.attach_to_cli(eut_console, log_file)
    clines.eut_get_operator(
        clines.eut_login,
        clines.eut_password,
        clines.eut_hostname,
        eut_1_spawn
    )
    install_promts = (
        '\]:|\]Mb:|\]MB:|' +
        clines.eut_login +
        "':"
    )
    list_of_input_commands = [
        'install image',  # In version VyOS 1.1 was 'install system'
        'Yes',
        'Auto',
        'sda',
        'Yes',
        '',
        '',
        '',
        clines.eut_password,
        clines.eut_password
    ]
    for command in list_of_input_commands:
        clines.eut_operator_send_raw_command(
            command,
            install_promts,
            eut_1_spawn
        )
    clines.eut_operator_send_raw_command(
        'sda',
        clines.eut_operator_promt,
        eut_1_spawn
    )

    clines.add_eut(clines.get_resource_body(eut_name, eut_console))
    clines.destroy_vm(eut_name)


if __name__ == '__main__':

    args = clines.parse_test_args(sys.argv[1:])
    log_file = args.log
    eut_name = args.eut_name
    eut_console = args.eut_console
    test_summary = args.test_summary
    weight = args.weight
    test(eut_name, eut_console, log_file)
