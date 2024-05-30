# Standard Lib Imports:
import os

# Package Imports:
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Register the blueprint (the controller) with flask!
    from . import simple_blueprint
    app.register_blueprint(simple_blueprint.bp)

    return app
