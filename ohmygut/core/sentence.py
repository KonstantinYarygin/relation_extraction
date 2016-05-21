class Sentence(object):

    def __init__(self, text, article_title, journal,
                 bacteria, nutrients, diseases,
                 parser_output, shortest_paths):
        super().__init__()
        self.shortest_paths = shortest_paths
        self.journal = journal
        self.text = text
        self.article_title = article_title
        self.parser_output = parser_output
        self.diseases = diseases
        self.nutrients = nutrients
        self.bacteria = bacteria

    def __repr__(self):
        out = self.text + '\n'
        out += 'diseases: ' + str(self.diseases) + '\n'
        out += 'nutrients: ' + str(self.nutrients) + '\n'
        out += 'bacteria: ' + str(self.bacteria) + '\n'
        return out
