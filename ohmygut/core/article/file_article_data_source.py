import os
import re
from lxml import etree
from ohmygut.core.article.article import Article
from ohmygut.core.article.article_data_source import ArticleDataSource


def get_articles_nxmls(articles_directory):
    """
    Yields articles full nxml in alphabetical order
    :param articles_directory:
    :return: generator
    """
    pathes = []
    for root, dirs, files in os.walk(articles_directory):
        for file in files:
            if not file.endswith('.nxml'):
                continue
            file_full_path = os.path.join(root, file)
            pathes.append(file_full_path)
    pathes.sort()
    for file_full_path in pathes:
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
                    for subelement in element.iter():
                        if subelement.tag in set(['italic', 'underline', 'bold', 'p']):
                            full_text_chunks.append(subelement.text)
                        full_text_chunks.append(subelement.tail)
    full_text_chunks = [chunk.strip() for chunk in full_text_chunks if chunk and len(chunk) != 1]
    full_text = ' '.join(full_text_chunks)
    full_text = full_text.replace(' )', ')')
    full_text = full_text.replace(' ;', ';')
    full_text = full_text.replace(' ,', ',')
    full_text = full_text.replace('\n', ' ')
    full_text = re.sub('\s?\([^\d\w]+\)', '', full_text)
    full_text = re.sub('\s?\[[^\d\w]+\]', '', full_text)
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


def get_article_journal(nxml):
    root = etree.XML(nxml)
    journal = ''
    for element in root.iter():
        if element.tag == 'journal-title':
            journal = element.text.lower()
    return journal


class FileArticleDataSource(ArticleDataSource):
    def __init__(self, articles_folder):
        super().__init__()
        self.articles_directory = articles_folder

    def get_articles(self):
        nxmls = get_articles_nxmls(self.articles_directory)
        for nxml in nxmls:
            text = get_article_text(nxml)
            title = get_article_title(nxml)
            journal = get_article_journal(nxml)
            yield Article(title, text, journal)
