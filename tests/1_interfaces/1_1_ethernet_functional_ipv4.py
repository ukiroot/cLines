import sys
import lib.clines as clines


def test():
    print(clines.get_bridges(bridges))
    print(clines.get_euts(euts))
    print(clines.get_linuxchans(linuxchans))


if __name__ == '__main__':

    args = clines.parse_test_args(sys.argv[1:])
    clines.eut_log_file = args.log
    bridges = args.bridges
    euts = args.euts
    linuxchans = args.linuxchans
    test_summary = args.test_summary
    topology = args.topology
    weight = args.weight
    clines.release_all_resource()
    test()
