class Article(object):
    # todo: add pmid
    def __init__(self, title, text, journal):
        super().__init__()
        self.journal = journal
        self.text = text
        self.title = title

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
