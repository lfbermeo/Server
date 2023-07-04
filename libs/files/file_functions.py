from base64 import b64encode as __b64encode
from io import BytesIO as __BytesIO
from os import path as __path
from typing import TypedDict as __TypedDict
from uuid import uuid4 as __uuid4

from PIL import Image as __Image
from werkzeug.datastructures import FileStorage as __FileStorage

from config import INPUT_FOLDER as __INPUT_FOLDER
from config import OUTPUT_FOLDER as __OUTPUT_FOLDER

UploadedFileType = __TypedDict('UploadedFileType', {
    'filename': str,
    'filepath': str
})


def __upload_file(file: __FileStorage) -> UploadedFileType:
    extension_file = file.content_type.split('/')[-1]
    filename = str(__uuid4()) + '.' + extension_file
    filepath = __path.join(__INPUT_FOLDER, filename)

    file.save(filepath)

    return {'filename': filename, 'filepath': filepath}


def upload_files(files: list[__FileStorage]) -> list[UploadedFileType]:
    # create_directory(INPUT_FOLDER, delete_content=True)

    result = []

    for file in files:
        if file:
            result.append(__upload_file(file))

    return result


def __encode_img(filepath: str) -> str:
    img = __Image.open(filepath, mode='r')
    buffered = __BytesIO()
    img.save(buffered, format='JPEG')
    img_base64 = __b64encode(buffered.getvalue()).decode('utf-8')

    return img_base64


def encode_imgs(filepaths: list[str]) -> list[str]:
    result = []

    for filepath in filepaths:
        result.append(__encode_img(filepath))

    return result


def __download_file(filename: str) -> str:
    filepath = __path.join(__OUTPUT_FOLDER, filename)
    img = __encode_img(filepath)
    return img


def download_files(filesnames: list[str]) -> list[str]:
    filepaths = [__path.join(__OUTPUT_FOLDER, filename)
                 for filename in filesnames]
    imgs = encode_imgs(filepaths)

    return imgs
