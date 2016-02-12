from nltk import sent_tokenize


def get_sentences(text):
    # todo: use stanford tokenizer
    return sent_tokenize(text)
