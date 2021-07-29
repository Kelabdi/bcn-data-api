from app import app
from flask import request
from utils.json_response import json_response
from utils.handle_error import handle_error


@app.route("/")
@handle_error
def ejemplo():
    print("terminal")
    print(request.args)
    name = request.args.get("name","")
    surname = request.args.get("surname")
    return {
        "name":name,
        "surname": surname
    }


@app.route("/read/<nombre>")
@handle_error
def ejemplo2(nombre):
    return {
        "name":nombre
    }
