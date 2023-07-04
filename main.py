#!/bin/env python

import config as cfg
from server import create_server
from server.routes import socketio

HOST = '127.0.0.1'

if __name__ == "__main__":
    print(f'Starting server on http://{HOST}:{cfg.PORT}/')
    server_app = create_server(debug=True)
    socketio.init_app(server_app, debug=True, cors_allowed_origins='*')
    socketio.run(server_app, host=HOST, port=cfg.PORT)
