from flask import request, jsonify
from google.cloud import vision
from flask import Flask
import base64

from style import Style

app = Flask(__name__)

import csv

# Dictionary of jsons. Keys are labels. Values are json {style: x, points: n}
mydict={}
for row in csv.reader(open('resources/labels.csv')):
    mydict[row[0]] = {'style': row[1], 'label': row[0], 'points': row[2]}

@app.route("/labels", methods=['POST'])
def get_labels():

    client = vision.Client()
    decoded_image = base64.b64decode(request.data)
    image = client.image(content=decoded_image)
    labels = image.detect_labels()
    style = Style(request.data)
    style.set_labels(labels)


    global mydict
    labels_json = {'Labels':[]}
    styles_json = {'Styles':[]}
    for label in labels:
        labels_json['Labels'].append(label.description)
        if (label.description) in mydict.keys():
            style = mydict[label.description]
            #print style
            styles_json['Styles'].append(style)

    for label in style.labels:
        print label
    response = jsonify(style.as_dict())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    app.run(debug=True, use_debugger=False, use_reloader=False)
