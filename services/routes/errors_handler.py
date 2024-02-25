from flask import jsonify, make_response
from . import routes

@routes.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
