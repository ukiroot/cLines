import json
import sys
import os
import datetime
import time
import subprocess
import lib.clines as clines


def prepare_parent_system():
    os.system(
        'bash ' +
        path_from_root +
        clines.slash_char +
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


def get_list_of_tests(config):
    with open(config, 'r') as f:
        config = json.load(f)[json_root]
    for group in config:
        for test in config[group]:
            peace_of_test_path = (
                group +
                clines.slash_char +
                test
            )
            test_path = (
                'tests/' +
                peace_of_test_path
            )
            for iteration_key in config[group][test]:
                iteration = config[group][test][iteration_key]
                print(type(iteration))
                print(iteration)
                args = []
                for arg_key, value in iteration.items():
                    args.append('--' + arg_key + '=' + value)
                iteration_log_path = (
                    '--log=logs/' +
                    timestamp +
                    peace_of_test_path +
                    clines.slash_char +
                    iteration_key +
                    '.log'
                )
                test_exec = [
                    python_inter,
                    test_path,
                    iteration_log_path,
                    *args
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
    timestamp = datetime.datetime.now().strftime('%Y/%m/%d_%H_%M/')
    list_of_services_proc = []
    list_of_active_tests = []
    path_from_root = os.path.abspath(os.path.dirname(sys.argv[0]))
    python_inter = '/usr/bin/python3'
    path_to_logs_dir = path_from_root + "/logs/"
    pool_log_file = path_to_logs_dir + "pool.log"
    pool_path = (
        path_from_root +
        clines.slash_char +
        'services/pool_of_resources.py'
    )
    config = (
        path_from_root +
        clines.slash_char +
        'configs/config_of_tests.json'
    )
    json_root = 'tests'
    #  Block of exeс
    clines.create_dir(path_to_logs_dir)
    pool_log = open(pool_log_file, 'w')
    proc = start_pool_of_resources(pool_log)
    list_of_services_proc.append({'pool': proc})
    prepare_parent_system()
    get_list_of_tests(config)
    #  Stop all services
    stop_services(list_of_services_proc)
