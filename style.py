import json


class Style(object):

    def __init__(self, stream):
        self.style = ''
        self.labels = {'labels': []}
        self.image_stream = stream

    def set_labels(self, labels):
        for label in labels:
            self.labels['labels'].append({'description': label.description, 'score': label.score})

    def as_json(self):
        return json.dumps(self.__dict__)