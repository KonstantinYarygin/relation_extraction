import os
os.chdir("/home/konstantin/documents/projects/python/text_mining/relation_extraction/")

from sentence_processing import SentenceProcessor
from collections import namedtuple
from itertools import product

Sentence = namedtuple('Sentence', ['text', 'bacteria', 'nutrients'])

with open('out_sent_test.txt') as f:
    data = [line.strip() for line in f.readlines()]
    sentences = data[::4]
    bacteria = [line.split(', ') for line in data[1::4]]
    nutrients = [line.split(', ') for line in data[2::4]]
    for n, record in enumerate(zip(sentences, bacteria)):
        sentence, bact_list = record
        bact_list_new = [bact.replace(' ', '-') for bact in bact_list]
        for bact, bact_new in zip(bact_list, bact_list_new):
            sentences[n] = sentences[n].replace(bact, bact_new)
        bacteria[n] = bact_list_new
    data = list(zip(sentences, bacteria, nutrients))
    data = [Sentence(*record) for record in data]

proc_sentences = [SentenceProcessor(record.text) for record in data]


for record, sent in list(zip(data, proc_sentences))[:]:
    pairs = product(record.bacteria, record.nutrients)
    print()
    print(repr(sent.sentence))
    if 'Graph' in dir(sent):
        for bact, nutr in pairs:
            out = sent.search_path(bact, nutr)
            if out:
                print(out['tags'])
                print(out['path'])

print(proc_sentences[-14].)
print(data[4])
print(proc_sentences[4].Graph.nodes())
print(proc_sentences[4].Graph.edges())
proc_sentences[0].Graph.draw()