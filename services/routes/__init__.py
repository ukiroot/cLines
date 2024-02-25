from flask import Flask
routes = Flask( __name__)

from .errors_handler import *
from .pool_of_resources import *
