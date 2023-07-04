from base64 import b64decode, b64encode
from io import BytesIO, StringIO
from typing import Any, Union

from PIL import Image


def decode_data_image(data_image: str) -> Union[Image.Image, None]:
    _, data = data_image.split(',')  # (headers) _ = 'data:image/jpeg;base64' | data = 'base64 string'
    buffer = StringIO()
    buffer.write(data)

    bytes_data = BytesIO(b64decode(data))

    try:
        img = Image.open(bytes_data)
        return img
    except OSError as ex:
        print(f"Error opening image: {ex}")
        return None
    except Exception as ex:
        print(f"Unexpected error: {ex}")
        return None


def encode_data_image(img_encode: Any) -> str:
    """
    Base64 encoding image for send via internet
    @param img_encode: cv2.imencode() result
    """
    string_data = b64encode(img_encode).decode('utf-8')
    return 'data:image/jpeg;base64,' + string_data
