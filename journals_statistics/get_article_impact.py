from lxml import etree
from collections import namedtuple
import csv
import sys
import os

with open('if2015.csv') as f:
    data = csv.reader(f.readlines(), delimiter='\t', quotechar='"')
    impact_by_title = {record[0].lower(): record[1] for record in data}

def get_nxmls(artiles_dir):
    for root, dirs, files in os.walk(artiles_dir):
        for file in files:
            if not file.endswith('.nxml'):
                continue
            file_full_path = os.path.join(root, file)
            with open(file_full_path) as f:
                article_nxml = ''.join(f.readlines())
            yield article_nxml

with open('title_journal_impact.tsv', 'w') as out:
    for article_nxml in get_nxmls('../../article_data/texts'):
        root = etree.XML(article_nxml)

        for element in root.iter():
            if element.tag == 'journal-title':
                journal = element.text.lower()
                if journal in impact_by_title:
                    impact = impact_by_title[journal]
                else:
                    impact = 'NO IMPACT'
        title = []
        root = etree.XML(article_nxml)
        for root_child in root.iter():
            if root_child.tag == 'article-meta':
                for element in root_child.iter():
                    if element.tag == 'article-title':
                        title.append(''.join(element.itertext()))
        title = ' '.join(title)

        out.write('\t'.join([title, journal, impact]) + '\n')