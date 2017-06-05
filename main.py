from flask import request, jsonify
from google.cloud import vision
from flask import Flask
import base64
from styles_comparator import StylesComparator

app = Flask(__name__)


@app.route("/labels", methods=['POST'])
def get_labels():
    client = vision.Client()
    decoded_image = base64.b64decode(request.data)
    image = client.image(content=decoded_image)
    labels_objects = image.detect_labels()
    labels = [str(label.description.lower()) for label in labels_objects]
    logos_objects = image.detect_logos()
    logos = [str(logo.description).lower() for logo in logos_objects]
    labels.extend(logos)
    style = StylesComparator(request.data)
    twin_response = style.find_twin(labels)
    style.save_new_image_and_labels(labels)
    if not twin_response:
        response = jsonify(style.create_error_output())
    else:
        response = jsonify(style.create_output(labels, twin_response))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    app.run(debug=True, use_debugger=False, use_reloader=False)
