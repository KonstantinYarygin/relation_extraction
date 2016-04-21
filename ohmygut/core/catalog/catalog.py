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
    def __init__(self, name, code, tag, additional_tags=None):
        super().__init__()
        if additional_tags is None:
            additional_tags = []
        self.additional_tags = additional_tags
        self.tag = tag
        self.code = code
        self.name = name

    def __repr__(self):
        return "%s;%s" % (self.name, self.code)


class EntityCollection(object):
    def __init__(self, entities, tag):
        super().__init__()
        self.tag = tag
        self.entities = entities

    def get_tag(self):
        return self.tag

    def __repr__(self):
        return ("%s" % str(self.entities)).replace('[', '').replace(']', '')


