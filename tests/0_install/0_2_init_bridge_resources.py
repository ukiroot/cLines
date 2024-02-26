import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import lib.clines as clines

def test(bridge_name):
    clines.add_bridge(clines.get_resource_body(bridge_name, ''))


if __name__ == '__main__':

    args = clines.parse_test_args(sys.argv[1:])
    clines.eut_log_file = args.log
    bridge_name = args.bridge_name
    test(bridge_name)
