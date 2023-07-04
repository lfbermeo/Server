from os import path as __path
from uuid import uuid4 as __uuid4

import cv2
from flask import Blueprint, Response

import config as cfg
from libs.detector import (PredictionResultType, YoloV8ModelMedium,
                           YoloV8ModelSmall, predict)
from server.responses import generic_response

yolo_routes = Blueprint('yolo_routes', __name__)

YOLO_SMA = YoloV8ModelSmall()
YOLO_MED = YoloV8ModelMedium()

predictions: list[PredictionResultType] = []


@yolo_routes.get('/image')
def predict_images() -> Response:
    global predictions
    predictions = []
    predict(source=cfg.INPUT_FOLDER, model=YOLO_MED, callback=predictions.append)

    return generic_response({'message': 'Ok', 'predictions': predictions})


@yolo_routes.get('/video')
def predict_video() -> Response:
    global predictions
    predictions = []

    predict(source=cfg.INPUT_FOLDER, model=YOLO_SMA, callback=predictions.append)

    prediction = predictions[-1]

    print(prediction)

    filepath = __path.join(cfg.OUTPUT_FOLDER, prediction['filename'])
    new_video_name = str(__uuid4()) + '.mp4'

    video_to_mp4(filepath, cfg.OUTPUT_FOLDER + "/" + new_video_name)

    prediction['filename'] = new_video_name
    return generic_response({'message': 'Ok', 'predictions': [prediction]})


def video_to_mp4(input: str, output: str, fps: int = 0, frame_size=(), fourcc: str = "H264") -> None:
    vidcap = cv2.VideoCapture(input)

    print(type(vidcap))

    if not fps:
        fps = round(vidcap.get(cv2.CAP_PROP_FPS))
    success, arr = vidcap.read()
    if not frame_size:
        height, width, _ = arr.shape
        frame_size = width, height
    writer = cv2.VideoWriter(
        output,
        apiPreference=0,
        fourcc=cv2.VideoWriter_fourcc(*fourcc),
        fps=fps,
        frameSize=frame_size,
    )
    while True:
        if not success:
            break
        writer.write(arr)
        success, arr = vidcap.read()
    writer.release()
    vidcap.release()
