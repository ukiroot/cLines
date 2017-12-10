import argparse


def parse_test_args(args):
    parser = argparse.ArgumentParser(
        description='Parser for tests arguments',
    )
    parser.add_argument(
        '--log',
        action="store",
        default='/dev/stdout',
        type=str
    )
    parser.add_argument(
        '--eut_name',
        action="store",
        type=str
    )
    parser.add_argument(
        '--eut_console',
        action="store",
        type=str
    )
    parser.add_argument(
        '--bridge_name',
        action="store",
        type=str
    )
    parser.add_argument(
        '--test_summary',
        action="store",
        type=str
    )
    parser.add_argument(
        '--weight',
        action="store",
        type=int
    )
    parser.add_argument(
        '--euts', '--EUTs',
        action="store",
        type=int
    )
    parser.add_argument(
        '--linuxchans',
        action="store",
        type=int
    )
    parser.add_argument(
        '--bridges',
        action="store",
        type=int
    )
    parser.add_argument(
        '--topology',
        action="store",
        type=str
    )
    return parser.parse_args(args)
