import csv
import re

from collections import namedtuple
from hash_tree import HashTree

class BacteriaCatalog(object):
    """Object holding NCBI ontology"""
    def __init__(self, nodes_path='./data/bacteria/taxdump/nodes.dmp',
                       names_path='./data/bacteria/taxdump/names.dmp',
                       verbose=True):
        """Creation of catalog object

        input:
            nodes_path: path to NCBI nodes.dmp file
            names_path: path to NCBI names.dmp file

        creates:
            self.scientific_names: dictionary with NCBI_id as key and scientific bacteria name as value
            self.bact_id_dict: dictionary with various versions of bacterial names as keys and NCBI_id as value
            self.hash_tree_root: root node of hash tree
        """
        if verbose:
            print('Creating bacterial catalog...')
        
        node_record = namedtuple('node_record', ['id', 'parent_id', 'rank'])
        name_record = namedtuple('name_record', ['id', 'name', 'unique_name', 'name_class'])

        name_class_exclusions = {'type material': True,
                                 'genbank acronym': True,
                                 'acronym': True}

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
        # rewrite using csv lib

        self.scientific_names = {record.id: record.name for record in name_data if record.name_class == 'scientific name'}
        self.bact_id_dict = {record.name: record.id for record in name_data}
        self.remove_bacteria_literally()

        self.generate_excessive_dictionary(node_data, name_data)

        self.hash_tree = HashTree(self.bact_id_dict.keys())


    def remove_bacteria_literally(self):
        """Removes from catalog 'bacteria' (name of kingdom) items =)"""
        del self.scientific_names['2'] # 2 - NCBI id of 'Bacteria'
        del self.bact_id_dict['bacteria']
        del self.bact_id_dict['Bacteria']


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
        # Strain name
        bact_short_names_dict = {record.name[0] + '. ' + record.name.split(' ')[1]: record.id for record in species_shortable_records}
        self.bact_id_dict.update(bact_short_names_dict)


    def find_bacteria(self, text):
        """ Uses previously generated hash tree to search text for bacterial names

        input:
            text: text to search for bacterial names

        returns:
            list of (bactrium_name, NCBI_id) tuples found in text
        """

        bact_names = self.hash_tree.search(text)
        bact_ids = [self.bact_id_dict[name] for name in bact_names]
        output_list = list(zip(bact_names, bact_ids))
        return(output_list)
