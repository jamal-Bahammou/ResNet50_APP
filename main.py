from flask import Flask, request, jsonify
from flask_cors import CORS
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image
import base64
import io

from keras.applications.resnet50 import ResNet50
from keras.applications.resnet50 import decode_predictions
import requests
from bs4 import BeautifulSoup


import tensorflow as tf
graph = tf.get_default_graph()


app = Flask(__name__)
CORS(app)


# IMPORT THE MODEL
print(" * Loading Keras model ...")
model = ResNet50(weights='imagenet')
print(" * Keras model loaded, is redy to use ...")


# PREPROCESS IMAGE TO FIT THE CNN MODEL
def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    return image


@app.route("/predict", methods=["POST"])
def predict():
    message = request.get_json(force=True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image, target_size=(224, 224))

    with graph.as_default():
        prediction = model.predict(processed_image)
        id = decode_predictions(prediction, top=1)[0][0][0]
        name = decode_predictions(prediction, top=1)[0][0][1]
        accuracy = decode_predictions(prediction, top=1)[0][0][2]

        page = requests.get("http://www.image-net.org/api/text/imagenet.synset.geturls?wnid="+id)
        soup = BeautifulSoup(page.content, 'html.parser')
        str_soup = str(soup)
        split_urls = str_soup.split('\r\n')
        split_urls = split_urls[0:20]
        images_list = []
        for i in range(20):
            if(split_urls[i][0:11] == 'http://farm'):
                images_list.append(split_urls[i])

    response = {
        'name': name,
        'accuracy': str(accuracy),
        'prediction': images_list
    }

    return jsonify(response)