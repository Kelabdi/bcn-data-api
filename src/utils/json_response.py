from bson.json_util import dumps, loads
from flask import Response

def json_response(data, status=200):
    return Response(
        dumps(data),
        mimetype="application/json"
    )

def str_to_json(data):
    return loads(data)