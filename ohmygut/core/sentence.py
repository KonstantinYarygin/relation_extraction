class Sentence(object):

    def __init__(self, text, article, entities_collections, parser_output, shortest_paths):
        super().__init__()
        self.article = article
        self.entities_collections = entities_collections
        self.shortest_paths = shortest_paths
        self.text = text
        self.parser_output = parser_output

    def __repr__(self):
        return self.text

