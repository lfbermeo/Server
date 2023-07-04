from os import listdir as __listdir
from os import path as __path
from pathlib import Path as __Path
from typing import Callable as __Callable
from typing import Literal as __Literal
from typing import TypedDict as __TypedDict

from libs.detector.models import (ModelBase, YoloV8ModelMedium,
                                  YoloV8ModelNano, YoloV8ModelSmall)

__all__ = ["ModelBase", "YoloV8ModelNano", "YoloV8ModelSmall", "YoloV8ModelMedium"]

BoxesType = __Literal["xyxy", "xywh"]

PredictionType = __TypedDict('PredictionType', {
    'conf': float,
    'box': list[float]
})
PredictionResultType = __TypedDict('PredictionResultType', {
    'filename': str,
    'predictions': list[PredictionType]
})


def get_list_files(dir_path: __Path | str) -> list[str]:
    files: list[str] = []

    for pathfile in __listdir(dir_path):
        if __path.isfile(__path.join(dir_path, pathfile)):
            files.append(pathfile)

    return files


def predict(source: __Path | str, model: ModelBase, box_type: BoxesType = "xyxy",
            callback: __Callable[[PredictionResultType], None] | None = None) -> None:
    filenames = get_list_files(source)

    results = model.detect(source)

    index = 0

    is_video = (len(filenames) == 1) and (filenames[index].split('.')[-1] == 'mp4')

    # Comprobar si es video o imagenes
    # La funcionalidad actual procesa un batch de imagenes

    boxes: list[list[float]] = []
    confs: list[float] = []
    prediction: PredictionResultType

    if not is_video:
        for result in results:
            if result.boxes is not None:
                # xyxy: Tensor = result.boxes.xyxy
                boxes = getattr(result.boxes, box_type).tolist()
                confs = result.boxes.conf.tolist()

                prediction = {
                    "filename": filenames[index],
                    "predictions": []
                }

                print(result.boxes.conf)

                for box, conf in zip(boxes, confs):
                    prediction["predictions"].append({"conf": conf, "box": box})

                if callable(callback):
                    callback(prediction)

                index += 1

    else:
        frame = 0
        for result in results:
            if result.boxes is not None:
                frame += 1

                boxes = getattr(result.boxes, box_type).tolist()
                confs = result.boxes.conf.tolist()

                predictions: list[PredictionType] = []

                for box, conf in zip(boxes, confs):
                    predictions.append({"conf": conf, "box": box})

                print(f'Frame {frame}: {predictions}')

                prediction = {
                    "filename": filenames[index],
                    "predictions": predictions
                }

                if callable(callback):
                    callback(prediction)
