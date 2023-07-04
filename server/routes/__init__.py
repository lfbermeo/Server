from server.routes.file_routes import file_routes
from server.routes.generic_routes import generic_routes
from server.routes.socket_routes import socketio
from server.routes.yolo_routes import yolo_routes

__all__ = ["generic_routes", "file_routes", "yolo_routes", "socketio"]
