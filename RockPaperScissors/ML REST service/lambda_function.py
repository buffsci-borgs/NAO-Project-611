from flask import Flask, render_template, request
from flask_cors import CORS
import urllib.request
import urllib.parse
import json

import tensorflow as tf
from tensorflow import keras
import h5py
import cv2
from PIL import Image
import numpy as np


def detectGesture(request):
    r = request
    nparr = np.fromstring(r.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('test.png', img)

    gesture = "test"
    npimg = np.array(img)
    npimg = npimg / 255.0
    x = np.expand_dims(npimg, axis=0)
    x = np.expand_dims(x, axis=3)
    model = keras.models.load_model('model05.h5')
    pred = model.predict(x)
    for i in range(3):
        if pred[0][i]*100 > 50:
            if i == 0:
                gesture = "Scissors"
            elif i == 1:
                gesture = "Paper"
            elif i == 2:
                gesture = "Rock"
            break
    # print(gesture)
    return {
        'statusCode': 200,
        'body': json.dumps(gesture)
    }

def lambda_handler(event, context):
    body = json.loads(event.get('body'))
    # detectGesture(event['queryStringParameters'])
    return {
        'statusCode': 200,
        'body': json.dumps(event['queryStringParameters'])
    }


