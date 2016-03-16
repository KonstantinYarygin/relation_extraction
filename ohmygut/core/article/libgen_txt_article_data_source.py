from ohmygut.core.article.article import Article
from ohmygut.core.article.article_data_source import ArticleDataSource
import os


def get_libgen_articles(libgen_folder):
    with open(os.path.join(libgen_folder, 'pmc_metadata.tsv')) as f:
        raw_metadata = [line.strip().split('\t') for line in f.readlines()]
        metadata = {PMC: (title, journal) for PMC, title, journal in raw_metadata}

    filenames = os.listdir(os.path.join(libgen_folder, 'txt'))
    filepathes = [os.path.join(libgen_folder, 'txt', _file) for _file in filenames]

    for filename, filepath in zip(filenames, filepathes):
        PMC = filename.split('.')[0]
        title, journal = metadata[PMC]
        with open(filepath) as f:
            file_lines = [line.strip('\n- ') for line in f.readlines()]
            text = ' '.join(file_lines)
        yield {'text': text, 'title': title, 'journal': journal}


class LibgenTxtArticleDataSource(ArticleDataSource):
    def __init__(self, libgen_folder):
        super().__init__()
        self.libgen_folder = libgen_folder

    def get_articles(self):
        libgen_articles = get_libgen_articles(self.libgen_folder)
        for libgen_article in libgen_articles:
            text = libgen_article['text']
            title = libgen_article['title']
            journal = libgen_article['journal']
            yield Article(title, text, journal)
