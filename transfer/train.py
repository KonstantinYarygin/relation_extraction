import datetime
import pickle
from random import shuffle

from gensim.models.doc2vec import TaggedDocument, Doc2Vec

SENTECES_FILE_PATH = "/home/anatoly/do/relation_extraction/data/sentences_labeled_replaced_no_disease.txt"


class SentenceDataSource(object):
    def __init__(self, filename):
        self.sentences = []
        for uid, line in enumerate(open(filename)):
            [text, label] = line.split("\t")
            self.sentences.append(TaggedDocument(words=text.split(), tags=[label]))

    def get_sentences_shuffled(self):
        shuffle(self.sentences)
        return self.sentences

    def get_sentences(self):
        return self.sentences

sentence_data_source = SentenceDataSource(SENTECES_FILE_PATH)
model = Doc2Vec(workers=3, size=200)
model.build_vocab(sentence_data_source.get_sentences())

print("start training")
for epoch in range(20):
    print("epoch %i" % epoch)
    model.train(sentence_data_source.get_sentences_shuffled())
print("finished training")

with open("model%s.pkl" % (datetime.datetime.now().strftime("%H_%M_%S-%d_%m_%y")), 'wb') as pickle_file:
    pickle.dump(model, pickle_file)

