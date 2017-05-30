from flask import request
from google.cloud import vision
from flask import Flask
import base64

from style import Style

app = Flask(__name__)


@app.route("/labels", methods=['POST'])
def get_labels():
    client = vision.Client()
    decoded_image = base64.b64decode(request.data)
    image = client.image(content=decoded_image)
    labels = image.detect_labels()
    style = Style(request.data)
    style.set_labels(labels)

    for label in style.labels['labels']:
        print label
    return style.as_json()

if __name__ == "__main__":
    app.run(debug=True, use_debugger=False, use_reloader=False)
