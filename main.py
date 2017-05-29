
import io

from flask import json
from google.cloud import vision
from flask import Flask

app = Flask(__name__)


@app.route("/labels")
def get_labels():
    client = vision.Client()
    file_name = 'resources/traje.jpg'

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
        image = client.image(content=content)

    # Performs label detection on the image file
    labels = image.detect_labels()

    labels_json = {'Labels':[]}
    for label in labels:
        labels_json['Labels'].append(label.description)
    return json.dumps(labels_json)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
