import os

from lxml import etree

from ohmygut.core.article.article import Article
from ohmygut.core.article.article_data_source import ArticleDataSource


def get_articles_nxmls(articles_directory):
    articles_folderpathes = (os.path.join(articles_directory, foldername) for foldername in
                             os.listdir(articles_directory))
    articles_filepathes = (os.path.join(folderpath, file) for folderpath in articles_folderpathes for file in
                           os.listdir(folderpath))
    articles_nxml_pathes = (filepath for filepath in articles_filepathes if filepath.endswith('.nxml'))
    for articles_nxml_path in articles_nxml_pathes:
        with open(articles_nxml_path) as f:
            article_nxml = ''.join(f.readlines())
        yield (articles_nxml_path, article_nxml)


def get_article_text(article_nxml):
    root = etree.XML(article_nxml)

    full_text = ''
    for root_child in root.iterchildren():
        if root_child.tag == 'body':
            for element in root_child.iter():
                if element.tag == 'p':
                    full_text += ''.join(element.itertext()) + ' '

    return full_text


class FileArticleDatasource(ArticleDataSource):
    def __init__(self, articles_folder):
        super().__init__()
        self.articles_directory = articles_folder

    def get_articles(self):
        paths_nxmls = get_articles_nxmls(self.articles_directory)
        for path_nxml in paths_nxmls:
            path = path_nxml[0]
            nxml = path_nxml[1]
            text = get_article_text(nxml)
            yield Article(path, text)
