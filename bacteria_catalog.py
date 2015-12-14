import csv
import re

from nltk.tokenize import word_tokenize
from collections import namedtuple

class TreeNode(object):
    """Hash tree node"""
    def __init__(self):
        self.is_end = False
        self.children = {}

class BacteriaCatalog(object):
    def __init__(self, nodes_path='./data/bacteria/taxdump/nodes.dmp',
                       names_path='./data/bacteria/taxdump/names.dmp'):
        """Creation of catalog object

        input:
            nodes_path: path to NCBI nodes.dmp file
            names_path: path to NCBI names.dmp file

        yelds:
            self.primary_names: dictionary with NCBI_id as key and scientific bacteria name as value
            self.bact_id_dict: dictionary with various versions of bacterial names as keys and NCBI_id as value
            self.hash_tree_root: root node of hash tree
        """

        node_record = namedtuple('node_record', ['id', 'parent_id', 'rank'])
        name_record = namedtuple('name_record', ['id', 'name', 'unique_name', 'name_class'])

        name_class_exclusions = {'type material': 0,
                                 'genbank acronym': 0,
                                 'acronym': 0}

        with open(nodes_path) as nodes:
            node_data = [line.strip('\t|\n').split('\t|\t') for line in nodes.readlines()]
            node_data = [record[:3] for record in node_data if record[4] == '0'] # 0 - bacteria
            node_data = [node_record(*record) for record in node_data]
            node_data = {record.id: record for record in node_data}

        with open(names_path) as names:
            name_data = [line.strip('\t|\n').split('\t|\t') for line in names.readlines()]
            name_data = [name_record(*record) for record in name_data]
            name_data = [record for record in name_data if record.id in node_data]
            name_data = [record for record in name_data if record.name_class not in name_class_exclusions]

        self.primary_names = {record.id: record.name for record in name_data if record.name_class == 'scientific name'}
        self.bact_id_dict = {record.name: record.id for record in name_data}
        del self.primary_names['2']
        
        self.generate_excessive_dictionary(node_data, name_data)
        del self.bact_id_dict['bacteria']
        del self.bact_id_dict['Bacteria']

        self.generate_hash_tree()


    def generate_excessive_dictionary(self, node_data, name_data):
        """Generate variuos types of bacterial names that can occur in text:
            - Abbreviation (e.g. 'H. pylori' from 'Helicobacter pylori')
            - Plural form (e.g. 'Streptococci' from 'Streptococcus') #NOT IMPLEMENTED YET#
           Put all generated forms in self.bact_id_dict
        """
        species_ids = {record.id: 0 for record in node_data.values() if record.rank == 'species'}
        species_shortable_records = [record for record in name_data if record.id in species_ids and \
                                                                       record.name.count(' ') == 1 and \
                                                                       record.name[0].isupper()]
        bact_short_names_dict = {record.name[0] + '. ' + record.name.split(' ')[1]: record.id for record in species_shortable_records}

        self.bact_id_dict.update(bact_short_names_dict)

    def generate_hash_tree(self):
        """Takes all bacterial names (from self.bact_id_dict) and generates structure for text search - hash tree

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

        yelds:
            self.hash_tree_root: root node of hash tree            
        """

        self.hash_tree_root = TreeNode()
        list_names = [name.split(' ') for name in self.bact_id_dict.keys()]

        for list_name in list_names:
            current_node = self.hash_tree_root
            for word in list_name:
                if word not in current_node.children:
                    current_node.children[word] = TreeNode()
                current_node = current_node.children[word]
            current_node.is_end = True

    def find_bacteria(self, text):
        """ Uses previously generated hash tree to search text for bacterial names

        input:
            text: text to search for bacterial names

        returns:
            list of bactrium_name - NCBI_id tuples found in text
        """

        # list_text = text.split(' ')
        list_text = word_tokenize(text)
        bact_names = []

        for i, word in enumerate(list_text):
            if word in self.hash_tree_root.children:
                bact_name = ''
                current_node = self.hash_tree_root.children[word]
                search_next = True
                j = i
                while search_next:
                    j += 1
                    if j >= len(list_text):
                        if current_node.is_end:
                            bact_name = list_text[i:j]
                        break
                    search_next = False
                    if list_text[j] in current_node.children:
                        current_node = current_node.children[list_text[j]]
                        search_next = True
                    elif current_node.is_end:
                        bact_name = list_text[i:j]
                if bact_name:
                    bact_names.append(' '.join(bact_name))

        bact_ids = [self.bact_id_dict[name] for name in bact_names]
        output_list = list(zip(bact_names, bact_ids))
        return(output_list)
