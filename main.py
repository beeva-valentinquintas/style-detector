import json
import os
import time
from flask import request, jsonify
from flask_cors import cross_origin
from google.cloud import vision
from flask import Flask
import base64
import io
from PIL import Image
from google.cloud.vision.feature import FeatureTypes, Feature

from os.path import join, dirname

from styles_comparator import StylesComparator

app = Flask(__name__)


@app.route("/labels", methods=['POST'])
@cross_origin()
def get_labels():
    client = vision.Client()
    decoded_image = base64.b64decode(request.data)
    image = client.image(content=decoded_image)

    all_data = image.detect([Feature(FeatureTypes.FACE_DETECTION),
                             Feature(FeatureTypes.LABEL_DETECTION),
                             Feature(FeatureTypes.LOGO_DETECTION)])
    labels = [str(label.description).lower() for label in all_data[0].labels]
    logos = [str(logo.description).lower() for logo in all_data[0].logos]
    faces = [face for face in all_data[0].faces]
    labels.extend(logos)

    save_labels_and_image(decoded_image, all_data[0].labels)

    style = StylesComparator(request.data)
    twin_response = style.find_twin(labels)
    style.save_new_image_and_labels(labels)
    if not twin_response:
        response = jsonify(style.create_error_output())
    else:
        response = jsonify(style.create_output(labels, twin_response))
    response.status_code = 200
    return response


def save_labels_and_image(decoded_image, labels_objects):
    if not os.path.exists(join(dirname(__file__), "test_images")):
        os.mkdir(join(dirname(__file__), "test_images"))
    labels_with_scores = [{"label": str(label.description.lower()), "score": label.score} for label in labels_objects]
    timestamp = str(time.time())
    filename = join(dirname(__file__), "test_images", timestamp)
    with open(filename, 'w') as fd:
        json.dump(labels_with_scores, fd)
    filename += '_image'
    image = Image.open(io.BytesIO(decoded_image))
    image.save(filename, format="JPEG")


if __name__ == "__main__":
    app.run(debug=True, use_debugger=False, use_reloader=False)
