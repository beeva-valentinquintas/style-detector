import os

import io
from google.cloud import vision
import argparse
import sys

FILENAME='resources/traje.jpg'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-filename", help='filename')
    args = parser.parse_args()
    if args.filename is None:
        parser.print_help()
        sys.exit(-1)
    return args

def main():

    args = parse_args()

    client = vision.Client()

    # The name of the image file to annotate
    file_name = os.path.join(
        os.path.dirname(__file__),args.filename
        )

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
        image = client.image(
            content=content)

    # Performs label detection on the image file
    labels = image.detect_labels()

    print('Labels:')
    for label in labels:
        print(label.description)

if __name__ == "__main__":
    main()
