import abc


class Catalog(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def initialize(self):
        raise NotImplementedError("Method have to be implemented")

    @abc.abstractmethod
    def find(self, sentence_text):
        """
        :param sentence_text:
        :return: Entity
        """
        raise NotImplementedError("Method have to be implemented")

    @abc.abstractmethod
    def get_list(self):
        raise NotImplementedError("Method have to be implemented")


class Entity(object):
    def __init__(self, name, code, tag):
        super().__init__()
        self.tag = tag
        self.code = code
        self.name = name


class EntityCollection(object):
    def __init__(self, entities, tag):
        super().__init__()
        self.tag = tag
        self.entities = entities

    def get_tag(self):
        return self.tag
