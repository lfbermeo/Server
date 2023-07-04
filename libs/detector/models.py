from pathlib import Path
from typing import Any, Iterator, cast

from ultralytics import YOLO
from ultralytics.yolo.engine.results import Results


class ModelBase():
    def __init__(self, model: str | Path = 'yolov8n.pt') -> None:
        self._model: YOLO = YOLO(model)
        self._config = {
            'conf': 0.6,
            'iou': 0.45,
            'classes': 0,
            'save': True,
            'visualize': False,
            'project': 'temp',
            'name': 'output',
            'exist_ok': True,
            'stream': True
        }

    @property
    def model(self) -> YOLO:
        return self._model

    @property
    def config(self) -> dict[str, Any]:
        return self._config

    # autopep8: off
    def detect(self, source: Any | None) -> Iterator[Results] | list[Results]: # type: ignore[empty-body]
        pass
    # autopep8: on


class YoloV8ModelNano(ModelBase):
    def __init__(self) -> None:
        super().__init__(model=Path("models", "worker-helmet-8n.pt"))

    def detect(self, source: Any | None) -> list[Results]:
        override_config = self._config.copy()
        override_config['save'] = False
        override_config['stream'] = False
        override_config['classes'] = [0, 1]

        return cast(list[Results], self._model.predict(
            source=source,
            **override_config
        ))


class YoloV8ModelSmall(ModelBase):
    def __init__(self) -> None:
        super().__init__(model=Path("models", "worker-helmet-8s.pt"))

    def detect(self, source: Any | None) -> Iterator[Results]:
        return cast(Iterator[Results], self._model.predict(
            source=source,
            **self._config
        ))


class YoloV8ModelMedium(ModelBase):
    def __init__(self) -> None:
        super().__init__(model=Path("models", "worker-helmet-8m.pt"))

    def detect(self, source: Any | None) -> Iterator[Results]:
        return cast(Iterator[Results], self._model.predict(
            source=source,
            **self._config
        ))
