from flask import Blueprint, Response

from server.responses import generic_response

generic_routes = Blueprint('generic_routes', __name__)


@generic_routes.get('/')
def index() -> Response:
    return generic_response('Welcome to detector helmet API')


@generic_routes.get('/ping')
def ping() -> Response:
    return generic_response('Ok API is ready!')
