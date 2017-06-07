import io
import requests
import sys
import time
from PIL import Image
from google.cloud import vision
from os.path import join

from image_manager import ImageManager
from styles_comparator import StylesComparator
from vision_service import VisionService

filename = 'resources/hipster.jpg'

MOCK_LABELS = False

if len(sys.argv) == 3:
    filename = sys.argv[2]
else:
    print "Usage: test.py -f filename\n"
    sys.exit(0)

print "Filename is {}".format(filename)
data = open(filename, 'rb').read()


def test1(data):

    decoded_image = data

    if not MOCK_LABELS:

        image_manager = ImageManager()
        client = vision.Client()

        vision_service = VisionService(client, image_manager)
        labels = vision_service.find_features(decoded_image)
    else:
        labels = ['clothing', 'puma', 'star wars']

    print labels
    style = StylesComparator(data)
    res = style.create_output_for_user(style.image_stream, labels)
    return res["styles"]


def test2(data):

    import base64
    data64 = base64.b64encode(data)
    res = requests.post(url='http://localhost:5000/labels',
                    data=data64,
                    headers={'Content-Type': 'application/octet-stream'})
    return res.json()['myself']['styles']


def test3(data):
    import base64
    data64 = base64.b64encode(data)
    res = requests.post(url='http://localhost:5000/labels',
                    data=data64,
                    headers={'Content-Type': 'application/octet-stream'})

    twin = res.json()['twin']['image']
    image = Image.open(io.BytesIO(base64.b64decode(twin)))
    image.save(join("/tmp/", str(time.time())), format="JPEG")

print test3(data)
#print test2(data)
