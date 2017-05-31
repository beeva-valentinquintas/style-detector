import csv


class Style(object):

    def __init__(self, stream):
        self.styles = []
        self.labels = []
        self.image_stream = stream

    def set_labels(self, labels):
        valid_styles = {}
        for row in csv.reader(open('resources/labels.csv')):
            valid_styles[row[0]] = {'style': row[1], 'label': row[0], 'points': row[2]}

        for label in labels:
            if label.description in valid_styles.keys():
                style = valid_styles[label.description]
                self.styles.append(style)
                self.labels.append({'description': label.description, 'score': label.score})

    def as_dict(self):
        return self.__dict__
