import cv2
from flask_socketio import SocketIO as __SocketIO
from flask_socketio import emit

from libs.detector import YoloV8ModelNano
from libs.processes.image_procedures import (decode_data_image,
                                             encode_data_image)

socketio = __SocketIO()

model_var: YoloV8ModelNano | None = None


@socketio.on('connect')
def test_connect():
    print('Client connected')
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    # emit('my response', {'data': 'Disconnected'})


@socketio.on('message')
def handle_message(message):
    print(f'Received message: {message}')
    emit('my response', {'data': message})


@socketio.on('load-model')
def load_model():
    global model_var

    if model_var is None:
        model_var = YoloV8ModelNano()
        print(model_var)

        model_info = "Yolov8 Nano Model summary: 225 layers, 3011433 parameters, 0 gradients, 8.2 GFLOPs"
        emit('model-loaded', {'info': model_info})
    else:
        emit('model-loaded', {'info': 'Model already loaded'})


@socketio.on('predict')
def predict_io(img_data: str):
    global model_var
    print('Enter to "predict" socket event')

    if model_var is None:
        emit('model-not-loaded', {'info': 'Model not loaded'})
        print('Model not loaded')
        return

    img_decoded = decode_data_image(img_data)

    if img_decoded is not None:
        results = model_var.detect(img_decoded)

        annotated_frame = results[0].plot()

        classes = [int(n) for n in results[0].boxes.cls.tolist()]  # [0.0, 1.0] --> [0, 1]

        if len(classes) == 0:
            person_with_helmet = 'NOTHING'
        elif len(classes) == 1:
            person_with_helmet = 'WITH_HELMET' if classes[0] == 0 else 'WITHOUT_HELMET'
        else:
            person_with_helmet = 'WITH_HELMET' if len({0, 1}.difference(set(classes))) == 0 else 'WITHOUT_HELMET'

        print(f'Classes: {classes}')
        print(f'Person with helmet: {person_with_helmet}')

        cv2_coded = cv2.imencode('.jpg', annotated_frame)[1]

        encoded_image = encode_data_image(cv2_coded)

        emit('predicted', {
            'imgData': encoded_image,
            'predictions': len(classes),
            'classes': classes,
            'personWithHelmet': person_with_helmet
        })
