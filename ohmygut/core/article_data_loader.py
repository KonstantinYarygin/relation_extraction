import os
from nltk.tokenize import sent_tokenize
from nltk.tokenize.stanford import StanfordTokenizer
from lxml import etree


def get_articles_nxmls(articles_directory):
    articles_folderpathes = (os.path.join(articles_directory, foldername) for foldername in
                             os.listdir(articles_directory))
    articles_filepathes = (os.path.join(folderpath, file) for folderpath in articles_folderpathes for file in
                           os.listdir(folderpath))
    articles_nxml_pathes = (filepath for filepath in articles_filepathes if filepath.endswith('.nxml'))
    for articles_nxml_path in articles_nxml_pathes:
        with open(articles_nxml_path) as f:
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

    full_text_sentences = [sent for chunk in full_text_chunks for sent in sent_tokenize(chunk)]
    return full_text_sentences
