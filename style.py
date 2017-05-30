class Style(object):

    def __init__(self, stream):
        self.style = ''
        self.labels = []
        self.image_stream = stream

    def set_labels(self, labels):
        for label in labels:
            self.labels.append({'description': label.description, 'score': label.score})

    def as_dict(self):
        return self.__dict__
