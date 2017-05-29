import os

import io
from google.cloud import vision


def main():
    client = vision.Client()

    # The name of the image file to annotate
    file_name = 'resources/traje.jpg'

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
        image = client.image(content=content)

    # Performs label detection on the image file
    labels = image.detect_labels()

    print('Labels:')
    for label in labels:
        print(label.description)

if __name__ == "__main__":
    main()
