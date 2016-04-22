import datetime
import os

import pickle
import re

from ohmygut.core.constants import TRIM_LETTERS_NUMBER, RESULT_DIR_NAME
from ohmygut.core.write.base_writer import BaseWriter


def delete_forbidden_characters(string):
    return_string = string.replace(' ', '_')
    return_string = re.sub('[^\w_\d\.]', '', return_string)
    return return_string


class PklWriter(BaseWriter):

    def __init__(self, output_dir):
        super().__init__()
        self.output_dir = output_dir
        self.sentence_number = 0

    def write(self, sentence):
        self.sentence_number += 1
        filename = '%s_%s_%i.pkl' % (sentence.journal[0:TRIM_LETTERS_NUMBER],
                                     sentence.article_title[0:TRIM_LETTERS_NUMBER],
                                     self.sentence_number)
        filename = delete_forbidden_characters(filename)
        filename = os.path.join(self.output_dir, filename)
        with open(filename, 'wb') as f:
            pickle.dump(sentence, f)


def get_output_dir_path():
    output_dir = os.path.join(RESULT_DIR_NAME, "pickled_%s" % datetime.datetime.now().strftime("%d%b%Y-%H-%M-%S"))
    os.mkdir(output_dir)
    return output_dir
