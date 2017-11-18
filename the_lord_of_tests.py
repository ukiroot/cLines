import json
import sys
import os
import datetime
from lib import euts


def prepare_parent_system():
    os.system(
        'bash ' +
        path_from_root +
        euts.slash_char +
        'scripts/shell/init_system.bash'
    )


def prepare_test_exec(command):
    command = command.replace('[', '"')
    command = command.replace(']', '"')
    command = command.replace("'", "")
    return command


def get_list_if_tests(config):
    with open(config, 'r') as f:
        config = json.load(f)[json_root]
    for group in config:
        for test in config[group]:
            for iteration in config[group][test]:
                peace_of_test_path = (
                    group +
                    euts.slash_char +
                    test
                )
                test_path = (
                    ' tests/' +
                    peace_of_test_path
                )
                iteration_log_path = (
                    ' logs/' +
                    timestamp +
                    peace_of_test_path +
                    euts.slash_char +
                    iteration +
                    '.log'
                )
                test_exec = (
                    python_inter +
                    test_path +
                    iteration_log_path +
                    euts.space_char +
                    str(config[group][test][iteration]['args_name']) +
                    euts.space_char +
                    str(config[group][test][iteration]['args_value'])
                )
                test_exec = prepare_test_exec(test_exec)
                os.system(test_exec)



if __name__ == '__main__':
    timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M/')
    path_from_root = os.path.abspath(os.path.dirname(sys.argv[0]))

    python_inter = '/usr/bin/python3'
    json_root = 'tests'
    config = (
        path_from_root +
        euts.slash_char +
        'configs/config_of_tests.json'
    )
    prepare_parent_system()
    get_list_if_tests(config)
