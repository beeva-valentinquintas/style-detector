import csv

import pandas
from os.path import dirname, join


class StylesComparator(object):

    def __init__(self, stream):
        self.image_stream = stream
        self.valid_styles = self.get_valid_styles()

    @staticmethod
    def get_valid_styles():
        valid_styles = {}
        for row in csv.reader(open(join(dirname(__file__), 'resources', 'labels.csv'))):
            valid_styles[row[0]] = {'style': row[1], 'label': row[0], 'points': row[2], 'feature': row[3]}
        return valid_styles

    def save_new_image_and_labels(self, labels):
        data_store = open(join(dirname(__file__), 'resources', 'datastore'), 'a')
        for label in labels:
            if label in self.valid_styles.keys():
                valids = self.valid_styles[label]
                style = [valids['style'], valids['label'], valids['points'], self.image_stream+"\n"]
                style_string = ",".join(style)
                data_store.write(style_string)
        data_store.close()

    def filter_labels(self, labels):
        hipster_labels = self.divide_labels_by_style("hipster", labels, self.valid_styles)
        business_labels = self.divide_labels_by_style("business", labels, self.valid_styles)
        sport_labels = self.divide_labels_by_style("sport", labels, self.valid_styles)
        geek_labels = self.divide_labels_by_style("geek", labels, self.valid_styles)
        labels = hipster_labels
        labels.extend(business_labels)
        labels.extend(sport_labels)
        labels.extend(geek_labels)
        return labels

    def find_twin(self, labels):
        coincidences = []
        df = pandas.read_csv(join(dirname(__file__), 'resources', 'datastore'),
                             header=None, names=["style", "label", "points", "image"])
        others_labels = df.groupby('image')['label'].apply(list).values
        for other in others_labels:
            coincidences.append(set(other).intersection(set(labels)))
        if not coincidences:
            return None
        (index, better_list) = max(enumerate(coincidences), key=lambda tup: len(tup[1]))
        image = df.iloc[index].values[3]
        return self.create_output_for_user(image, better_list)

    def create_output(self, myself_labels, twin_output):
        return {
            "myself": self.create_output_for_user(self.image_stream, myself_labels),
            "twin": twin_output
        }

    @staticmethod
    def create_error_output():
        return {"message": "Couldn't find any similarities"}

    def create_output_for_user(self, image, labels):
        hipster_labels = self.divide_labels_by_style("hipster", labels, self.valid_styles)
        business_labels = self.divide_labels_by_style("business", labels, self.valid_styles)
        sport_labels = self.divide_labels_by_style("sport", labels, self.valid_styles)
        geek_labels = self.divide_labels_by_style("geek", labels, self.valid_styles)
        return {
            "styles": [
                {
                    "style": "hipster",
                    "labels": hipster_labels,
                    "points": self.calculate_points(hipster_labels)
                },
                {
                    "style": "business",
                    "labels": business_labels,
                    "points": self.calculate_points(business_labels)
                },
                {
                    "style": "sport",
                    "labels": sport_labels,
                    "points": self.calculate_points(sport_labels)
                },
                {
                    "style": "geek",
                    "labels": geek_labels,
                    "points": self.calculate_points(geek_labels)
                }
            ],
            "image": image
        }

    @staticmethod
    def divide_labels_by_style(style, labels, valid_styles):
        valid_labels = valid_styles.keys()
        labels_by_style = list(set([valid_styles[label]['feature'] for label in labels if label in valid_labels and valid_styles[label]['style'] == style]))
        return labels_by_style

    def calculate_points(self, labels):
        points = 0
        for label in labels:
            points += int(self.valid_styles[label]['points'])
        return points
