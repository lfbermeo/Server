from os import path

from flask import Blueprint, Response, request, send_from_directory

import config as cfg
from libs.files import remove_files_in_directory, upload_files
from server.responses import generic_response

file_routes = Blueprint('file_routes', __name__)


@file_routes.get('/<path:filename>')
def get_file(filename: str) -> Response:
    return send_from_directory(path.abspath(cfg.OUTPUT_FOLDER), path=filename, as_attachment=False)


@file_routes.post('/upload')
def upload() -> Response:
    if request.method != 'POST':
        return generic_response('Only POST method is allowe', 405)

    if 'file' not in request.files:
        return generic_response('No file part', 400)

    files = request.files.getlist('file')

    if any(file.filename == '' for file in files):
        return generic_response('No file selected', 400)

    remove_files_in_directory(cfg.INPUT_FOLDER)
    remove_files_in_directory(cfg.OUTPUT_FOLDER)

    filepaths = upload_files(files)

    if not filepaths:
        return generic_response('No file uploaded', 400)

    return generic_response({'message': 'Ok', 'filepaths': filepaths})
