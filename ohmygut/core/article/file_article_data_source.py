import os
from lxml import etree
from ohmygut.core.article.article import Article
from ohmygut.core.article.article_data_source import ArticleDataSource


def get_articles_nxmls(articles_directory):
    for root, dirs, files in os.walk(articles_directory):
        for file in files:
            file_full_path = os.path.join(root, file)
            with open(file_full_path) as f:
                article_nxml = ''.join(f.readlines())
            yield article_nxml


def get_article_text(article_nxml):
    root = etree.XML(article_nxml)

    full_text_chunks = []
    for root_child in root.iterchildren():
        if root_child.tag == 'body':
            for element in root_child.iter():
                if element.tag == 'p':
                    full_text_chunks.append(''.join(element.itertext()))
    full_text = ' '.join(full_text_chunks)
    return full_text


def get_article_title(article_nxml):
    title = []
    root = etree.XML(article_nxml)
    for root_child in root.iter():
        if root_child.tag == 'article-meta':
            for element in root_child.iter():
                if element.tag == 'article-title':
                    title.append(''.join(element.itertext()))
    title = ' '.join(title)
    return title


class FileArticleDataSource(ArticleDataSource):
    def __init__(self, articles_folder):
        super().__init__()
        self.articles_directory = articles_folder

    def get_articles(self):
        nxmls = get_articles_nxmls(self.articles_directory)
        for nxml in nxmls:
            text = get_article_text(nxml)
            title = get_article_title(nxml)
            yield Article(title, text)
