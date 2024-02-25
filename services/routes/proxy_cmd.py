import os
from flask import jsonify, abort, request
from . import routes

@routes.route('/restapi/v1.0/cmd_by_http', methods=['POST'])
def proxy_cmd():
    if not request.json or not ('cmd') in request.json:
        abort(400)
    cmd = request.json['cmd']
    # TO DO: create list of restrict commands and symbols
    result = os.system(cmd)
    return jsonify({"Return code": result}), 201