# Standard Lib Imports:
import os
import re
import json
from dataclasses import asdict
from typing import Any

# Package Imports:
from flask import (
    Blueprint, request, Response, current_app
)

# Local Imports:
from acptutorialpy.data.pizza import Pizza
from acptutorialpy.data.restaurant import Restaurant
from acptutorialpy.data.student import Student

bp = Blueprint('simple_blueprint', __name__)

@bp.route("/isAlive")
def is_alive() -> str:
    """Checks if the server is running."""
    return "I am running!"

@bp.route("/studentID/<string:id>", methods=["GET"])
def test_path_variable(id) -> str:
    """
    Given a student ID passed into the endpoint, returns the student ID back.
    
    Args:
        id (str): A student ID.
    
    Returns:
        str: A string with the student ID.
    """
    return f"Your Student ID is: {id}"

@bp.route("/postBody", methods=["POST"])
def test_post_with_body() -> dict[str, str] | Response:
    """
    Collects parameters from the body of the request creates a Student, logs the attributes and returns the posted object.
    
    Request Body:
        {
            "name": "Your Name Here",
            "student_id": "sXXXXXXX"
        }

    Returns:
        dict: A dictionary with the attributes of the Student.
    """
    # If the request header is application/json, try make the student.
    try:
        student = Student(**request.json)
    except TypeError as error:
        return Response("Invalid JSON values in your request", status=400)
    
    current_app.logger.info(f"Student Posted in body of request: {student}")
    return asdict(student)

@bp.route("/getQuery", methods=["GET"])
def test_get_with_query() -> str:
    """
    Collects parameters from the query string in the request and prints them.
    
    Args:
        param1 (str): A string to be printed.
        param2 (str): A string to be printed.
    
    Returns:
        str: A string with the parameters from the query string.
    """
    param_1 = request.args.get("param1")
    param_2 = request.args.get("param2")
    return f"You have posted in the query parameters: Param 1: {param_1}, Param 2: {param_2}"   

def from_camel_to_snake(dict_to_convert: dict[Any, Any]) -> dict[Any, Any]:
    """
    Converts camelCase keys into snake_case keys in a dictionary so any code generated in Java will work
    with Python snakecase.

    Args:
        dict_to_convert (dict): A dictionary with camelCase keys.
    
    Returns:
        dict: A dictionary with snake_case keys, used to create python objects.
    """
    for key in list(dict_to_convert.keys()):
        if any(x.isupper() for x in key):
            dict_to_convert[re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()] = dict_to_convert.pop(key)
        # Menu is a list of Pizza objects, we need to also convert the pizza objects keys as well!
        if key == "menu":
            dict_to_convert["menu"] = [from_camel_to_snake(pizza) for pizza in dict_to_convert["menu"]]
            
    current_app.logger.debug(f"Converted Dictionary: {dict_to_convert}")
    return dict_to_convert

@bp.route("/restaurants", methods=["GET"])
def get_restaurants() -> list[Restaurant] | Response:
    """
    Returns a response body with all the restaurants we have stored in the JSON file in our resources.

    Returns:
        list[Restaurant]: A list of Restaurant objects.
    """
    # Collect the pathname.
    file_path = os.path.join(os.path.dirname(__file__), "resources/restaurants.json")
    try:
        with open(file=file_path, mode="r") as file:
            restaurants = json.load(file) 
            # Alter the keys so they are snake_case to create the Restaurant objects.
            return [Restaurant(**from_camel_to_snake(restaurant)) for restaurant in restaurants]
    except FileNotFoundError as error:
        return Response("No restaurants found", status=404)
    

