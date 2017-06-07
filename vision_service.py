from google.cloud.vision.feature import FeatureTypes, Feature
import re

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

        annotations = image.detect_web()
        entities = [str(re.sub(r'[^\x00-\x7F]+',' ', entity.description)).lower() for entity in annotations.web_entities]
        #print entities
        labels.extend(entities)
        #self.report(entities)
        self.image_manager.save_labels(saved_image_path, all_data[0].labels)
        return labels

    def reduce_image_around_person(self, decoded_image):
        image = self.client.image(content=decoded_image)
        faces_objects = image.detect_faces()

        saved_image_path = self.image_manager.save_image(decoded_image)
        cropped_image = self.image_manager.crop_image_by_face(saved_image_path, faces_objects)
        if cropped_image is None:
            return decoded_image, saved_image_path
        return cropped_image, saved_image_path


    def report(self,annotations):
        """Prints detected features in the provided web annotations."""
        # [START print_annotations]

        if annotations.web_entities:
            print ('\n{} Web entities found: '.format(
            len(annotations.web_entities)))

            for entity in annotations.web_entities:
                print('Score      : {}'.format(entity.score))
                print('Description: {}'.format(entity.description))
        # [END print_annotations]
