from google.cloud.vision.feature import FeatureTypes, Feature


class VisionService(object):

    def __init__(self, visio_client, image_manager):
        self.client = visio_client
        self.image_manager = image_manager

    def find_features(self, image):
        cropped_image, saved_image_path = self.reduce_image_around_person(image)
        image = self.client.image(content=cropped_image)
        all_data = image.detect([Feature(FeatureTypes.LABEL_DETECTION, max_results=100),
                                 Feature(FeatureTypes.LOGO_DETECTION, max_results=100)])
        labels = [str(label.description).lower() for label in all_data[0].labels]
        logos = [str(logo.description).lower() for logo in all_data[0].logos]
        labels.extend(logos)
        self.image_manager.save_labels(saved_image_path, all_data[0].labels)
        return labels

    def reduce_image_around_person(self, decoded_image):
        image = self.client.image(content=decoded_image)
        faces_objects = image.detect_faces()

        saved_image_path = self.image_manager.save_image(decoded_image)
        cropped_image = self.image_manager.crop_image_by_face(saved_image_path, faces_objects)
        return cropped_image, saved_image_path
