import pickle

with open('/home/anatoly/do/relation_extraction/transfer/model17_44_18-07_03_16.pkl', 'rb') as f:
    model = pickle.load(f)
# pickle.load("")
# model = Doc2Vec()
# model.load_word2vec_format("/home/anatoly/do/relation_extraction/transfer/doc2vec.mmodel.w2c")
model.most_similar()
