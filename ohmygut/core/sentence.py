class Sentence(object):

    def __init__(self, text, article_title, journal, entities_collections, parser_output, shortest_paths):
        super().__init__()
        self.entities_collections = entities_collections
        self.shortest_paths = shortest_paths
        self.journal = journal
        self.text = text
        self.article_title = article_title
        self.parser_output = parser_output

    def __repr__(self):
        return self.text

