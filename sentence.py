class Sentence(str):
    """docstring for Sentence"""
    def __init__(self, raw_sentence):
        self.text = raw_sentence

    def __repr__(self):
        return self.text