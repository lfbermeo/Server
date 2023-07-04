from typing import Any
from flask import jsonify, Response


def generic_response(data: Any, status_code: int = 200) -> Response:
    if isinstance(data, str):
        response = jsonify({'message': data})
    else:
        response = jsonify({'data': data})

    response.status_code = status_code
    return response
