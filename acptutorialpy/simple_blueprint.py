# Standard Lib Imports:
import os

# Package Imports:
from flask import Blueprint

# Local Imports:
from .data.pizza import Pizza

bp = Blueprint('simple_blueprint', __name__)

@bp.route("/isAlive")
def isalive():
    return "I am running!"

# Rest of the endpoints will go here. 
