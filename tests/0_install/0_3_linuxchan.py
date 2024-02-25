import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import lib.clines as clines

ENVIRONMENT_IP=os.environ.get('ENVIRONMENT_IP')

def test(linuxchan_name, console, log_file):
    try:
        clines.start_vm(linuxchan_name)
        linuxchan_1_spawn = clines.attach_to_cli(console, log_file)
        clines.linuxchan_grub(linuxchan_name, linuxchan_1_spawn)
        clines.linuxchan_get_shell(linuxchan_name, linuxchan_1_spawn)
        clines.add_linuxchan(clines.get_resource_body(linuxchan_name, ''))
    finally:
        clines.destroy_vm(linuxchan_name)


if __name__ == '__main__':
    args = clines.parse_test_args(sys.argv[1:])
    log_file = args.log
    linuxchan_name = args.linuxchan_name
    console = args.eut_console
    print(args.linuxchan_name)
    test(linuxchan_name, console, log_file)
