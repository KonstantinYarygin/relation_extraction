import abc


class ArticleDataSource(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_articles(self):
        raise NotImplementedError("Method have to be implemented")
