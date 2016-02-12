class Sentence(object):

    def __init__(self, text, article_title, bacteria, nutrients, diseases, parse_result):
        super().__init__()
        self.parse_result = parse_result
        self.diseases = diseases
        self.nutrients = nutrients
        self.bacteria = bacteria
        self.article_title = article_title
        self.text = text

    def __repr__(self):
        return self.text