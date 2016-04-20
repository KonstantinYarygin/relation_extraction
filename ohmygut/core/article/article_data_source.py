import abc


class ArticleDataSource(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_articles(self):
        """

        :return: a generator which yields article texts
        """
        raise NotImplementedError("Method have to be implemented")
