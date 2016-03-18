import os
import re
from ohmygut.core.article.article import Article
from ohmygut.core.article.article_data_source import ArticleDataSource


def get_medline_records(medline_file):
    with open(medline_file) as f:
        lines = (line.rstrip('\n') for line in f.readlines())
        raw_data = []
        [raw_data[-1].append(line) if line else raw_data.append([]) for line in lines]

    for raw_record in raw_data:
        medline_record = {}
        for line in raw_record:
            m = re.match('^([A-Z]{1,4})\s{0,3}\-\s(.+)', line)
            if m:
                index = m.group(1)
                if index not in medline_record:
                    medline_record[index] = []
                medline_record[index].append(m.group(2).strip())
            else:
                medline_record[index][-1] += ' ' + line.strip()
        yield medline_record


class MedlineAbstractsArticleDataSource(ArticleDataSource):
    def __str__(self):
        return "medline abstracts article data source"

    def __init__(self, medline_file):
        super().__init__()
        self.medline_file = medline_file

    def get_articles(self):
        medline_records = get_medline_records(self.medline_file)
        for medline_record in medline_records:
            if 'AB' in medline_record:
                text = ''.join(medline_record['AB'])
            else:
                text = ''
            if 'TI' in medline_record:
                title = ''.join(medline_record['TI'])
            else:
                title = ''
            if 'JT' in medline_record:
                journal = ''.join(medline_record['JT'])
            else:
                journal = ''
            yield Article(title, text, journal)
