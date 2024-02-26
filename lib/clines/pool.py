import requests
import json
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "./"))
from chars import *
import configs.env

rest_service_url = 'http://{}:5000/restapi/v1.0/'.format(configs.env.ENVIRONMENT_IP)
pool_url = rest_service_url + 'pool/'
pool_url_eut = pool_url + 'eut'
pool_url_bridge = pool_url + 'bridge'
pool_url_linuxchan = pool_url + 'linuxchan'
transaction_url = rest_service_url + 'transaction'
transaction_status_key = 'status'
content_type_header = {"Content-Type": "application/json"}

def resapi_request(method, uri, body='', headers='', debug=False):
    method = method.upper()
    data = json.dumps(body)
    if method == 'PUT':
        response = requests.put(uri, data, headers=headers)
    elif method == 'POST':
        response = requests.post(uri, data, headers=headers)
    elif method == 'GET':
        response = requests.get(uri, headers=headers)
    elif method == 'DELETE':
        response = requests.delete(uri, headers=headers)
    else:
        print(method + " is wrong HTTP method or not implemented in func")
        return False
    if debug is True:
        print("Status_code:")
        print(response.status_code)
        print("Response_body:")
        print(response.text)
    return response


def add_resource(uri, body):
    resapi_request('POST', uri, body, {"Content-Type": "application/json"})


def update_resource(uri, body):
    resapi_request('PUT', uri, body, {"Content-Type": "application/json"})


def get_resource(uri):
    response = resapi_request('GET', uri)
    return response


def add_eut(body):
    add_resource(pool_url_eut, body)


def add_bridge(body):
    add_resource(pool_url_bridge, body)


def add_linuxchan(body):
    add_resource(pool_url_linuxchan, body)


def get_eut():
    return lock_resource(pool_url_eut, 'eut')


def get_bridge():
    return lock_resource(pool_url_bridge, 'bridge')


def get_linuxchan():
    return lock_resource(pool_url_linuxchan, 'linuxchan')


def lock_resource(url, resource_type):
    response = get_resource(url)
    for resource in json.loads(response.text)[resource_type]:
        if resource['available'] is True:
            resource['available'] = False
            url_instance = pool_url_eut + slash_char + str(resource['id'])
            update_resource(url_instance, resource)
            return resource


def release_all_resource():
    for url, resource_type in zip(
            [pool_url_eut, pool_url_bridge, pool_url_linuxchan],
            ['eut', 'bridge', 'linuxchan']
    ):
        response = get_resource(url)
        for resource in json.loads(response.text)[resource_type]:
            if resource['available'] is False:
                resource['available'] = True
                url_instance = pool_url_eut + slash_char + str(resource['id'])
                update_resource(url_instance, resource)


def count_available(url, resource_type):
    count = 0
    response = get_resource(url)
    for resource in json.loads(response.text)[resource_type]:
        if resource['available'] is True:
            count = count + 1
    return count


def get_available_eut():
    return count_available(pool_url_eut, 'eut')


def get_available_bridge():
    return count_available(pool_url_bridge, 'bridge')


def get_available_linuxchan():
    return count_available(pool_url_linuxchan, 'linuxchan')


def release_eut(body):
    release_resource(body, pool_url_eut)


def release_bridge(body):
    release_resource(body, pool_url_bridge)


def release_linuxchan(body):
    release_resource(body, pool_url_linuxchan)


def release_resource(body, url):
    body['available'] = True
    update_resource(url + slash_char + str(body['id']), body)


def get_resource_body(name, settings):
    body = {
                'name': name,
                'settings': [settings]
            }
    return body


def check_transaction():
    response = get_resource(transaction_url)
    status = json.loads(response.text)[transaction_status_key]
    if status == 'available':
        return True
    return False


def update_transaction(status, who=''):
    body = {'status': status}
    if who != '':
        body.update({'who': who})
    print(body)
    update_resource(transaction_url, body)


def set_transaction(who=''):
    update_transaction('processing', who)


def commit_transaction(who=''):
    update_transaction('available', who)


def get_bridges(qantity):
    list = []
    for i in range(qantity):
        list.append(get_bridge())
    return list


def get_euts(qantity):
    list = []
    for i in range(qantity):
        list.append(get_eut())
    return list


def get_linuxchans(qantity):
    list = []
    for i in range(qantity):
        list.append(get_linuxchan())
    return list
