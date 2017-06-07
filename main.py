from flask import request, jsonify
from flask_cors import cross_origin
from google.cloud import vision
from flask import Flask
import base64
from image_manager import ImageManager
from styles_comparator import StylesComparator
from vision_service import VisionService

app = Flask(__name__)


@app.route("/labels", methods=['POST'])
@cross_origin()
def get_labels():
    decoded_image = base64.b64decode(request.data)
    image_manager = ImageManager()
    client = vision.Client()

    vision_service = VisionService(client, image_manager)
    labels = vision_service.find_features(decoded_image)
    style = StylesComparator(request.data)
    labels = style.filter_labels(labels)
    twin_response = style.find_twin(labels)
    style.save_new_image_and_labels(labels)
    return generate_response(labels, style, twin_response)


def generate_response(labels, style, twin_response):
    if not twin_response:
        response = jsonify(style.create_error_output())
    else:
        response = jsonify(style.create_output(labels, twin_response))
    response.status_code = 200
    return response


if __name__ == "__main__":
    app.run(debug=True, use_debugger=False, use_reloader=False)
