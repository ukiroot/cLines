import requests
import json
from .chars import *

pool_url = 'http://127.0.0.1:5000/restapi/v1.0/pool/'
pool_url_eut = pool_url + 'eut'
pool_url_bridge = pool_url + 'bridge'
pool_url_linuxchan = pool_url + 'linuxchan'


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
            url_intance = pool_url_eut + slash_char + str(resource['id'])
            update_resource(url_intance, resource)
            return resource


def return_eut(body):
    return_resource(pool_url_eut, url)


def return_bridge(body):
    return_resource(pool_url_bridge, url)


def return_linuxchan(body):
    return_resource(pool_url_linuxchan, url)


def return_resource(body, url):
    body['available'] = True
    update_resource(url + slash_char + str(body['id']), body)


def add_bridge(body):
    add_resource(pool_url_bridge, body)


def get_resource_body(name, settings):
    body = {
                'name': name,
                'settings': [settings]
            }
    return body
