import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import lib.clines as clines

def pretest():
    clines.init_topology(euts, linuxchans, bridges, topology)

def posttest():
    clines.destroy_topology(euts, linuxchans)


def test():
    try:
        pretest()
    finally:
        posttest()


if __name__ == '__main__':
    args = clines.parse_test_args(sys.argv[1:])
    clines.eut_log_file = args.log
    bridges = clines.get_bridges(args.bridges)
    euts = clines.get_euts(args.euts)
    linuxchans = clines.get_linuxchans(args.linuxchans)
    topology = args.topology
    test_summary = args.test_summary
    weight = args.weight

    clines.release_all_resource()

    test()

#    "1_1_ethernet_functional_ipv4.py": {
#        "iteration_1": {
#            "EUTs" : "1",
#            "linuxchans" : "1",
#            "bridges" : "1",
#            "topology" : "eth0:br0,eth1:br0,eth2:br0,eth3:br0|eth0:br0",
#            "weight": "1"
#        }
#    }