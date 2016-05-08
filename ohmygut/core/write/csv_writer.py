import datetime
import os

import pandas as pd

from ohmygut.core.constants import RESULT_DIR_NAME
from ohmygut.core.write.base_writer import BaseWriter

INCLUDE_HEADER = True
CSV_SEPARATOR = '\t'


class CsvWriter(BaseWriter):
    def __init__(self, csv_path):
        super().__init__()
        self.csv_path = csv_path
        self.header_included = False

    def write(self, sentence):
        rows = []
        columns_part_1 = ['text', 'article_title', 'journal']
        columns_part_2_entities = []
        for collection in sentence.entities_collections:
            columns_part_2_entities.append(collection.tag.lower())
        columns_part_3 = ['length', 'from', 'to', 'tagfrom', 'tagto', 'words', 'tags', 'allwords', 'alltags', 'graph']

        columns = columns_part_1 + columns_part_2_entities + columns_part_3
        if INCLUDE_HEADER and not self.header_included:
            header_data = pd.DataFrame(columns=columns)
            header_data.to_csv(self.csv_path, mode='a', header=INCLUDE_HEADER, index=False, sep=CSV_SEPARATOR)
            self.header_included = True

        for paths in sentence.shortest_paths.values():
            for path in paths:
                tags = path.tags
                words = path.words
                length = len(path.nodes_indexes)
                name_from = path.words[0]
                name_to = path.words[-1]
                tag_from = path.tags[0]
                tag_to = path.tags[-1]
                row = [
                    sentence.text,
                    sentence.article_title,
                    sentence.journal]
                for collection in sentence.entities_collections:
                    row.append(str(collection))

                row = row + [
                    length,
                    name_from,
                    name_to,
                    tag_from,
                    tag_to,
                    words,
                    tags,
                    sentence.parser_output.words,
                    sentence.parser_output.tags,
                    sentence.parser_output.nx_graph.adj]
                rows.append(row)
        data = pd.DataFrame(rows, columns=columns)

        # todo: header writes also!
        data.to_csv(self.csv_path, mode='a', header=False, index=False, sep=CSV_SEPARATOR)


def get_csv_path():
    path = os.path.join(RESULT_DIR_NAME,
                        "result_%s.csv" % datetime.datetime.now().strftime("%d%b%Y-%H-%M-%S"))
    return path
