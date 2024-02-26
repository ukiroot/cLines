import os
from flask import jsonify, abort, request
from . import routes

@routes.route('/restapi/v1.0/cmd_by_http', methods=['POST'])
def cmd_by_http():
    if not request.json or not ('cmd') in request.json:
        abort(400)
    cmd = request.json['cmd']
    # TO DO: create list of restrict commands and symbols
    result = os.system(cmd)
    return jsonify({"Return code": result}), 201

@routes.route('/restapi/v1.0/get_vm_interfaces', methods=['POST'])
def get_vm_interfaces():
    if not request.json or not ('vm') in request.json:
        abort(400)
    vm = request.json['vm']
    # TO DO: create list of restrict commands and symbols for check VM
    cmd = '{} {} {}'.format('sudo virsh domiflist ', vm, "| grep vnet | awk '{print $1}'| xargs echo -n")
    interfaces = os.popen(cmd).read()
    return jsonify({"interfaces": interfaces}), 201