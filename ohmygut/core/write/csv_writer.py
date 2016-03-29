import datetime
import os

import pandas as pd

from ohmygut.core.constants import RESULT_DIR_NAME
from ohmygut.core.write.base_writer import BaseWriter

DO_INCLUDE_HEADER = True
CSV_SEPARATOR = '\t'


class CsvWriter(BaseWriter):
    def __init__(self, csv_path):
        super().__init__()
        self.csv_path = csv_path
        self.columns = ['text', 'article_title', 'journal',
                        'bacteria', 'nutrients', 'diseases', 'food']

        if DO_INCLUDE_HEADER:
            header_data = pd.DataFrame(columns=self.columns)
            header_data.to_csv(self.csv_path, mode='a', header=DO_INCLUDE_HEADER, index=False, sep=CSV_SEPARATOR)

    def write(self, sentence):
        values = [sentence.text,
                  sentence.article_title,
                  sentence.journal,
                  str(sentence.bacteria),
                  str(sentence.nutrients),
                  str(sentence.diseases),
                  str(sentence.food)]

        data = pd.DataFrame([values],
                            columns=self.columns)

        data.to_csv(self.csv_path, mode='a', header=False, index=False, sep=CSV_SEPARATOR)


def get_csv_path():
    path = os.path.join(RESULT_DIR_NAME,
                        "result_%s.csv" % datetime.datetime.now().strftime("%H_%M_%S-%d_%m_%y"))
    return path
