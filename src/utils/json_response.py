import json
from flask import Response

def json_response(data, status=200):
    return Response(
        json.dumps(data),
        mimetype="application/json"
    )
