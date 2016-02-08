import os

from nltk.tokenize import sent_tokenize
from itertools import islice
from lxml import etree


class Article(object):
    """General article data

    title - list of title sentences
    abstract - list of abstract sentences
    full_text - list of text sentences
    """
    def __init__(self, title, abstract, full_text=''):
        self.title = title
        self.abstract = abstract
        self.full_text = full_text

    def __repr__(self):
        """returns 'pretty' title and abstract"""
        out = ' === %s === \n' % str(self.title)
        out += str(self.abstract) + '\n'
        # out += str(self.full_text) + '\n'
        out += '\n'
        return(out)


class ArticleCatalog(object):
    """Generator containing objects of 'Article' class"""
    def __init__(self, path):
        """Process article data from .xml with abstracts of from folder
        containing folders with full article information

        input:
            path: path to .xml file or to folder

        creates:
            self.article_gen: generator yielding 'Article' class items
        """
        if os.path.isfile(path) and path.endswith('.xml'):
            self.type = 'abstract'
        elif os.path.isdir(path):
            self.type = 'full'
        else:
            self.type = None

        if self.type == 'full':
            article_folderpathes = (os.path.join(path, foldername) for foldername in os.listdir(path))
            filepathes = (os.path.join(folderpath, file) for folderpath in article_folderpathes for file in os.listdir(folderpath))
            nxml_filepathes = (filepath for filepath in filepathes if filepath.endswith('.nxml'))
            self.article_gen = (self.nxml_article_parse(nxml_filepath) for nxml_filepath in nxml_filepathes)
        elif self.type == 'abstract':
            tree = etree.parse(path)
            root =  tree.getroot()
            pubmed_article_records = (child for child in root)

            medline_citation_records = (record.find('MedlineCitation') for record in pubmed_article_records)
            medline_citation_records = (record for record in medline_citation_records if record)
            self.article_gen = (self.xml_abstracts_parse(record) for record in medline_citation_records)
        else:
            raise Exception("Incorrect path")

    def __getitem__(self, key):
        """Handling class like iterator with slices"""
        if isinstance(key, int):
            article = next(islice(self.article_gen, key, key + 1))
            return article
        elif isinstance(key, slice):
            article_list_iter = islice(self.article_gen, key.start, key.stop, key.step)
            return article_list_iter

    def xml_abstract_parse(self, medline_citation_record):
        """Get article data from .xml file single article record

        input:
            one medline citation record from .xml file containing abstracts

        returns:
            element of 'Article' class with:
            - title
            - abstract
        """
        article_record = medline_citation_record.find('Article')

        title = [article_record.find('ArticleTitle').text]
        
        abstract_record = article_record.find('Abstract')
        abstract_record_chunks = abstract_record.findall('AbstractText') if abstract_record else []
        abstract_chunks = [sub_record.text for sub_record in abstract_record_chunks if sub_record.text]
        abstract = sent_tokenize(' '.join(abstract_chunks))

        article = Article(title=title, abstract=abstract)
        return article
        
    def nxml_article_parse(self, path):
        """Get article data from single .nxml file

        input:
            path: path to .nxml file

        returns:
            element of 'Article' class with:
            - title
            - abstract
            - full_text
        """
        tree = etree.parse(path)
        root = tree.getroot()
        
        title = []
        for root_child in root.iter():
            if root_child.tag == 'article-meta':
                for element in root_child.iter():
                    if element.tag == 'article-title':
                        title.append(''.join(element.itertext()))
        title = [''.join(title)]

        abstract_chunks = []
        for root_child in root.iter():
            if root_child.tag == 'abstract':
                for element in root_child.iter():
                    if element.tag == 'p':
                        abstract_chunks.append(''.join(element.itertext()))
        abstract = [sent for chunk in abstract_chunks for sent in sent_tokenize(chunk)]
        abstract = [sent.replace('\n', ' ').strip() for sent in abstract]

        full_text_chunks = []
        for root_child in root.iterchildren():
            if root_child.tag == 'body':
                for element in root_child.iter():
                    if element.tag == 'p':
                        full_text_chunks.append(''.join(element.itertext()))
        full_text = [sent for chunk in full_text_chunks for sent in sent_tokenize(chunk)]
        full_text = [sent.replace('\n', ' ').strip() for sent in full_text]
        # join upper 3 parts into one block or function

        article = Article(title=title, 
                          abstract=abstract,
                          full_text=full_text)
        return article

# AC = ArticleCatalog('../data/texts')
# AC[2]