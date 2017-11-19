import json
import sys
import os
import datetime
import time
import subprocess
from lib import euts


def prepare_parent_system():
    os.system(
        'bash ' +
        path_from_root +
        euts.slash_char +
        'scripts/shell/init_system.bash'
    )


def start_pool_of_resources(log):
    return subprocess.Popen(
        [
            python_inter,
            pool_path
        ],
        stdout=log,
        stderr=log
    )


def stop_services(list_of_services):
    for service in list_of_services:
        service_proc = (service.get(*service))
        service_proc.kill()


def prepare_test_exec(command):
    command = command.replace('[', '')
    command = command.replace(']', '')
    command = command.replace("'", "")
    return command


def get_list_of_tests(config):
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
                    'tests/' +
                    peace_of_test_path
                )
                iteration_log_path = (
                    'logs/' +
                    timestamp +
                    peace_of_test_path +
                    euts.slash_char +
                    iteration +
                    '.log'
                )
                args_name = str(config[group][test][iteration]['args_name'])
                args_value = str(config[group][test][iteration]['args_value'])
                test_exec = [
                    python_inter,
                    test_path,
                    iteration_log_path,
                    prepare_test_exec(args_name),
                    prepare_test_exec(args_value)
                ]
                list_of_active_tests.append(subprocess.Popen(test_exec))
    while True:
        print("len of tests is " + str(len(list_of_active_tests)))
        if len(list_of_active_tests) != 0:
            for test_proc in list_of_active_tests:
                print(test_proc)
                time.sleep(1)
                poll = test_proc.poll()
                if poll is None:
                    print(test_proc)
                    print(poll)
                    time.sleep(2)
                else:
                    print("Process" + "test_proc" + " is over")
                    list_of_active_tests.remove(test_proc)
        else:
            break


if __name__ == '__main__':
    #  Block of variables
    timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M/')
    list_of_services_proc = []
    list_of_active_tests = []
    path_from_root = os.path.abspath(os.path.dirname(sys.argv[0]))
    python_inter = '/usr/bin/python3'
    path_to_logs_dir = path_from_root + "/logs/"
    pool_log_file = path_to_logs_dir + "pool.log"
    pool_path = (
        path_from_root +
        euts.slash_char +
        'services/pool_of_resources.py'
    )
    config = (
        path_from_root +
        euts.slash_char +
        'configs/config_of_tests.json'
    )
    json_root = 'tests'
    #  Block of exeс
    euts.create_dir(path_to_logs_dir)
    pool_log = open(pool_log_file, 'w')
    proc = start_pool_of_resources(pool_log)
    list_of_services_proc.append({'pool': proc})
    prepare_parent_system()
    get_list_of_tests(config)
    #  Stop all services
    stop_services(list_of_services_proc)
