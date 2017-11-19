import sys
import os


def test():
    euts.init_bridge_interface(name)
    log_file.write("Bridge " + name + ' was created\n')
    log_file.write(settings + '\n')
    euts.add_bridge(euts.get_resource_body(name, settings))


if __name__ == '__main__':
    sys.path.append(
        os.path.abspath(os.path.dirname(sys.argv[0])) +
        '/../../lib'
    )
    import euts
    test_args_values = sys.argv[3].split(', ')
    test_args_names = sys.argv[2].split(', ')
    log_file = euts.create_file(sys.argv[1])
    name = test_args_values[0]
    settings = test_args_values[1]
    test()
