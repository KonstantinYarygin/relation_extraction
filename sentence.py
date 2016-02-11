class Sentence(str):
    """docstring for Sentence"""
    def __init__(self, sentence):
        self.text = sentence

    def __repr__(self):
        return self.text