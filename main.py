
import io

from flask import json
from google.cloud import vision
from flask import Flask

app = Flask(__name__)

import csv

# Dictionary of jsons. Keys are labels. Values are json {style: x, points: n}
mydict={}
for row in csv.reader(open('resources/labels.csv')):
    mydict[row[0]] = {'style': row[1], 'label': row[0], 'points': row[2]}

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

    global mydict
    labels_json = {'Labels':[]}
    styles_json = {'Styles':[]}
    for label in labels:
        labels_json['Labels'].append(label.description)
        if (label.description) in mydict.keys():
            style = mydict[label.description]
            #print style
            styles_json['Styles'].append(style)
    return json.dumps(styles_json)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
