from nltk import word_tokenize


# TODO: test me

class _TreeNode(object):
    """Hash tree node"""

    def __init__(self):
        self.is_end = False
        self.children = {}


class HashTree(object):
    """Hash tree - structure for text search

        === EXAMPLE ===
        Hash tree for following strings:
            'aaa'
            'bbb'
            'bbb ccc'
            'bbb ggg'
            'bbb ddd eee'
            'bbb ddd fff'
        Will looks like:
                    |-- aaa*   |-- ccc*  |-- fff*
             ROOT --|          |         |
                    |-- bbb* --|-- ddd --|-- eee*
                               |
                               |-- ggg*      
        * symbol means end of string
        Every node is hashed and links to its chilrens
        ===============
    """

    def __init__(self, entity_list):
        """Takes all entity names and generates hash tree

        creates:
            self.root: root node of hash tree            
        """

        self.root = _TreeNode()
        list_names = [name.split(' ') for name in entity_list]

        for list_name in list_names:
            current_node = self.root
            for word in list_name:
                if word not in current_node.children:
                    current_node.children[word] = _TreeNode()
                current_node = current_node.children[word]
            current_node.is_end = True

    def search(self, text):
        """
        Uses previously generated hash tree to search text for entity names
        :param text: text to search for entity names
        :return: list of entity_names found in text
        """
        list_text = word_tokenize(text)
        entity_names = []

        for i, word in enumerate(list_text):
            if word in self.root.children:
                entity_name = ''
                current_node = self.root.children[word]
                search_next = True
                j = i
                while search_next:
                    j += 1
                    if j >= len(list_text):
                        if current_node.is_end:
                            entity_name = list_text[i:j]
                        break
                    search_next = False
                    if list_text[j] in current_node.children:
                        current_node = current_node.children[list_text[j]]
                        search_next = True
                    elif current_node.is_end:
                        entity_name = list_text[i:j]
                if entity_name:
                    entity_names.append(' '.join(entity_name))
        # refactor upper code
        return entity_names

