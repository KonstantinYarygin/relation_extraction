import abc


class BaseWriter(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def write(self, sentence):
        raise NotImplementedError("Method have to be implemented")
