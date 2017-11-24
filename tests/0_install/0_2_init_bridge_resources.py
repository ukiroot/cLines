import sys
import os


def test(bridge_name):
    core.init_bridge_interface(bridge_name)
    # clines.eut_log_file.write("Bridge " + bridge_name + ' was created\n')
    # clines.eut_log_file.write(settings + '\n')
    add_bridge(get_resource_body(bridge_name, ''))


if __name__ == '__main__':
    sys.path.append(
        os.path.abspath(os.path.dirname(sys.argv[0])) +
        '/../../lib'
    )
    from clines import *
    import clines.ccore as core

    args = parse_test_args(sys.argv[1:])
    core.eut_log_file = args.log
    bridge_name = args.bridge_name
    test(bridge_name)
