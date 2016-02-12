class Article(object):
    def __init__(self, path, text):
        super().__init__()
        self.text = text
        self.path = path
