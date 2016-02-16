from collections import namedtuple
from time import time
import csv

from ohmygut.core.catalog.catalog import Catalog
from ohmygut.core.hash_tree import HashTree


class BacteriaCatalog(Catalog):
    """Object holding NCBI ontology"""

    def __init__(self, nodes_path, names_path):
        self.names_path = names_path
        self.nodes_path = nodes_path
        self.__scientific_names = None
        self.__bact_id_dict = None
        self.__hash_tree = None

    def initialize(self, verbose=False):
        """Creation of catalog object

        input:
            nodes_path: path to NCBI nodes.dmp file
            names_path: path to NCBI names.dmp file

        creates:
            self.__scientific_names: dictionary with NCBI_id as key and scientific bacteria name as value
            self.__bact_id_dict: dictionary with various versions of bacterial names as keys and NCBI_id as value
            self.hash_tree_root: root node of hash tree
        """
        t1 = time()
        if verbose:
            print('Creating bacterial catalog...')

        node_record = namedtuple('node_record', ['id', 'parent_id', 'rank'])
        name_record = namedtuple('name_record', ['id', 'name', 'unique_name', 'name_class'])

        name_class_exclusions = {'type material': True,
                                 'genbank acronym': True,
                                 'acronym': True}

        with open(self.nodes_path) as nodes_dmpfile:
            node_data = csv.reader((line.replace('\t', '') for line in nodes_dmpfile), delimiter='|')
            node_data = (record[:3] for record in node_data if record[4] == '0')  # 0 - bacteria
            node_data = (node_record(*record) for record in node_data)
            node_data = {record.id: record for record in node_data}

        with open(self.names_path) as names_dmpfile:
            name_data = csv.reader((line.replace('\t', '') for line in names_dmpfile), delimiter='|')
            name_data = (record[:-1] for record in name_data)
            name_data = (name_record(*record) for record in name_data)
            name_data = (record for record in name_data if record.id in node_data)
            name_data = [record for record in name_data if record.name_class not in name_class_exclusions]
        # rewrite using csv lib

        self.__scientific_names = {record.id: record.name for record in name_data if
                                   record.name_class == 'scientific name'}
        self.__bact_id_dict = {record.name: record.id for record in name_data}

        self.__generate_excessive_dictionary(node_data, name_data)

        self.__remove_bacteria_literally()
        self.__hash_tree = HashTree(self.__bact_id_dict.keys())

        t2 = time()
        if verbose:
            print('Done. Total time: %.2f sec.' % (t2 - t1))

    def __remove_bacteria_literally(self):
        """Removes from catalog 'bacteria' (name of kingdom) items =)"""
        del self.__scientific_names['2']  # 2 - NCBI id of 'Bacteria'
        del self.__bact_id_dict['Bacteria']
        del self.__bact_id_dict['Monera']
        del self.__bact_id_dict['Procaryotae']
        del self.__bact_id_dict['Prokaryota']
        del self.__bact_id_dict['Prokaryotae']
        del self.__bact_id_dict['bacteria']
        del self.__bact_id_dict['eubacteria']
        del self.__bact_id_dict['prokaryote']
        del self.__bact_id_dict['prokaryotes']

    def __generate_excessive_dictionary(self, node_data, name_data):
        """Generate variuos types of bacterial names that can occur in text:
            - Abbreviation (e.g. 'H. pylori' from 'Helicobacter pylori')
            - Plural form (e.g. 'Streptococci' from 'Streptococcus') #NOT IMPLEMENTED YET#

        Put all generated forms in self.__bact_id_dict
        """
        species_ids = {record.id: 0 for record in node_data.values() if record.rank == 'species'}
        species_shortable_records = [record for record in name_data if record.id in species_ids and \
                                     record.name.count(' ') == 1 and \
                                     record.name[0].isupper()]
        # Strain name
        bact_short_names_dict = {record.name[0] + '. ' + record.name.split(' ')[1]: record.id for record in
                                 species_shortable_records}
        self.__bact_id_dict.update(bact_short_names_dict)

    def find(self, sentence):
        """ Uses previously generated hash tree to search sentence for bacterial names

        input:
            sentence: sentence to search for bacterial names

        returns:
            list of (bactrium_name, NCBI_id) tuples found in sentence
            :param sentence:
        """

        bact_names = self.__hash_tree.search(sentence)
        bact_ids = [self.__bact_id_dict[name] for name in bact_names]
        output_list = list(zip(bact_names, bact_ids))
        return output_list

    def get_scientific_name(self, ncbi_id):
        return self.__scientific_names[ncbi_id]