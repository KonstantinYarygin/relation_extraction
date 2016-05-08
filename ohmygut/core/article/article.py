class Article(object):
    def __init__(self, title, text, journal, pmc):
        super().__init__()
        self.pmc = pmc
        self.journal = journal
        self.text = text
        self.title = title

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
