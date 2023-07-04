from flask import Flask
from flask_cors import CORS

import config as cfg
from libs.files import create_directory
from server.routes import file_routes, generic_routes, yolo_routes

create_directory(cfg.INPUT_FOLDER, delete_content=True)
create_directory(cfg.OUTPUT_FOLDER, delete_content=True)


def create_server(debug: bool = True) -> Flask:
    app = Flask(__name__)
    CORS(app, origins=['*'])
    app.debug = debug

    app.register_blueprint(generic_routes)
    app.register_blueprint(file_routes, url_prefix='/api/files')
    app.register_blueprint(yolo_routes, url_prefix='/api/predict')

    # socketio.init_app(app, cors_allowed_origins='*', async_mode="eventlet")
    # socketio.init_app(app, cors_allowed_origins='*')
    return app


__all__ = ["create_server"]
