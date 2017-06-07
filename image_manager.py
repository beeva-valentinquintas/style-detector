import json
import os
import time
import io
from PIL import Image
from io import BytesIO
from os.path import join, dirname


class ImageManager(object):

    @staticmethod
    def save_image(image):
        if not os.path.exists(join(dirname(__file__), "test_images")):
            os.mkdir(join(dirname(__file__), "test_images"))
        timestamp = str(time.time())
        filename = join(dirname(__file__), "test_images", timestamp) + '.jpg'
        image = Image.open(io.BytesIO(image))
        image.save(filename, format="JPEG")
        return filename

    @staticmethod
    def save_labels(filename, labels_objects):
        labels_with_scores = [{"label": str(label.description.lower()), "score": label.score} for label in
                              labels_objects]
        with open(filename[:-4], 'w') as fd:
            json.dump(labels_with_scores, fd)

    @staticmethod
    def crop_image_by_face(image_path, face_objects):
        x_delta = 0.8
        y_delta = 0.2
        img = Image.open(image_path)
        if len(face_objects) == 0:
            return None
        face_vertices = face_objects[0].bounds.vertices
        x0, y0, x2, y2 = (face_vertices[0].x_coordinate, face_vertices[0].y_coordinate,
                          face_vertices[2].x_coordinate, face_vertices[2].y_coordinate)
        width, height = img.size
        face_width = x2 - x0
        face_height = y2 - y0
        left_up_x = int(x0 - x_delta * face_width) if x0 >= x_delta * face_width else 0
        left_up_y = int(y0 - y_delta * face_height) if y0 >= y_delta * face_height else 0
        right_down_x = int(x2 + x_delta * face_width) if x2 + x_delta * face_width <= width else width
        cropped = img.crop((left_up_x, left_up_y, right_down_x, height))
        cropped_filename = image_path[:-4] + '_cropped.jpg'
        cropped.save(cropped_filename, format="JPEG")

        with BytesIO() as output:
            with Image.open(cropped_filename) as img:
                img.save(output, 'BMP')
            return output.getvalue()
