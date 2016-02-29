from collections import namedtuple
import csv
import sys
import os

with open('title_journal_impact.tsv') as f:
    data = [line.strip().split('\t') for line in f.readlines()]
    impact_data = {record[0]: record[1:] for record in data}

output_record = namedtuple('output_record', ['sentence', 'title', 'bacteria', 'nutrients', 'diseases'])

with open('../sentences.csv') as f:
    f.readline()
    data = csv.reader(f, delimiter=',')
    data = [record[:2] + list(map(eval, record[2:])) for record in data]
    data = [output_record(*record) for record in data]
    data = [record.title for record in data]

journal_list = [impact_data[title][0] for title in data if title in impact_data]
impact_list = [impact_data[title][1] for title in data if title in impact_data]

with open('journal_list.txt', 'w') as f:
    f.write('\n'.join(journal_list))
with open('impact_list.txt', 'w') as f:
    f.write('\n'.join(impact_list))