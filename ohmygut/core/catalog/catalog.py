import abc


class Catalog(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def initialize(self):
        raise NotImplementedError("Method have to be implemented")

    @abc.abstractmethod
    def find(self, sentence_text):
        raise NotImplementedError("Method have to be implemented")

    @abc.abstractmethod
    def get_list(self):
        raise NotImplementedError("Method have to be implemented")