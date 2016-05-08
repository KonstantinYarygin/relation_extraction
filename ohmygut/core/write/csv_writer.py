import datetime
import os

import pandas as pd

from ohmygut.core.constants import RESULT_DIR_NAME
from ohmygut.core.write.base_writer import BaseWriter

INCLUDE_HEADER = True
CSV_SEPARATOR = '\t'


class CsvWriter(BaseWriter):
    def __init__(self, csv_path, tags):
        super().__init__()
        self.tags = tags
        self.csv_path = csv_path
        columns_part_1 = ['text', 'article_title', 'journal', 'pmc']
        columns_part_2_entities = []
        # order is important
        for tag in self.tags:
            columns_part_2_entities.append(tag.lower())
        columns_part_3 = ['length', 'from', 'to', 'tagfrom', 'tagto', 'words', 'tags', 'allwords', 'alltags', 'graph']
        self.columns = columns_part_1 + columns_part_2_entities + columns_part_3

        if INCLUDE_HEADER:
            header_data = pd.DataFrame(columns=self.columns)
            header_data.to_csv(self.csv_path, mode='a', header=INCLUDE_HEADER, index=False, sep=CSV_SEPARATOR)

    def write(self, sentence):
        rows = []
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
                    sentence.article.title,
                    sentence.article.journal,
                    sentence.article.pmc]

                # tags follow the same order as columns
                for tag in self.tags:
                    tagged_collection_list = [collection for collection in sentence.entities_collections
                                              if collection.tag == tag]
                    if len(tagged_collection_list) > 1:
                        raise Exception("found more than one collection by tag: tags not unique error")

                    if len(tagged_collection_list) == 0:
                        row.append("")

                    if len(tagged_collection_list) == 1:
                        row.append(str(tagged_collection_list[0]))

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
        data = pd.DataFrame(rows, columns=self.columns)

        data.to_csv(self.csv_path, mode='a', header=False, index=False, sep=CSV_SEPARATOR)


def get_csv_path():
    path = os.path.join(RESULT_DIR_NAME,
                        "result_%s.csv" % datetime.datetime.now().strftime("%d%b%Y-%H-%M-%S"))
    return path
