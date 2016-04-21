from itertools import product, combinations
import networkx as nx

from ohmygut.core.catalog.diseases_catalog import DISEASE_TAG
from ohmygut.core.catalog.gut_bacteria_catalog import BACTERIA_TAG
from ohmygut.core.catalog.nutrients_catalog import NUTRIENT_TAG
from ohmygut.core.catalog.usda_food_catalog import FOOD_TAG


class ShortestPath:
    def __init__(self, edge_rels, words, tags, nodes_indexes):
        super().__init__()
        self.nodes_indexes = nodes_indexes
        self.tags = tags
        self.words = words
        self.edge_rels = edge_rels
        self.type = None


def search_shortest_path(parser_output, source_node_id, target_node_id, undirected=True):
    if undirected:
        G = parser_output.nx_graph.to_undirected()
    else:
        G = parser_output.nx_graph

    try:
        nodes_indexes = nx.dijkstra_path(G, source_node_id, target_node_id)
    except nx.exception.NetworkXNoPath:
        return

    edge_rels = [G[i][j]['rel'] for i, j in zip(nodes_indexes[:-1], nodes_indexes[1:])]
    words = [parser_output.words[i] for i in nodes_indexes]
    tags = [parser_output.tags[i] for i in nodes_indexes]
    return ShortestPath(edge_rels, words, tags, nodes_indexes)


def analyze_sentence(parser_output):
    bacteria_nodes_ids = [id for id, tag in parser_output.tags.items() if tag == BACTERIA_TAG]
    nutrients_nodes_ids = [id for id, tag in parser_output.tags.items() if tag == NUTRIENT_TAG]
    diseases_nodes_ids = [id for id, tag in parser_output.tags.items() if tag == DISEASE_TAG]
    food_nodes_ids = [id for id, tag in parser_output.tags.items() if tag == FOOD_TAG]

    tag_nodeids_tuples = zip((BACTERIA_TAG, NUTRIENT_TAG, DISEASE_TAG, FOOD_TAG),
                             (bacteria_nodes_ids, nutrients_nodes_ids, diseases_nodes_ids, food_nodes_ids)
                             )

    shortest_pathes = {}
    for entity_1, entity_2 in combinations(tag_nodeids_tuples, 2):
        tag_1, nodes_ids_1 = entity_1
        tag_2, nodes_ids_2 = entity_2
        pair_tag = '-'.join([tag_1, tag_2])
        shortest_pathes[pair_tag] = []

        for node_id_1, node_id_2 in product(nodes_ids_1, nodes_ids_2):

            shortest_path = search_shortest_path(parser_output, node_id_1, node_id_2)
            if not shortest_path:
                continue

            # THIS CODE ONLY FOR FURTHER ANALYSIS
            # pattern_verbs = pattern_finder.find_patterns(shortest_path,
            #                                              sentence.parser_output.nx_graph,
            #                                              sentence.parser_output.words)
            # if pattern_verbs:
            #     shortest_path.type = pattern_verbs

            shortest_pathes[pair_tag].append(shortest_path)

    return shortest_pathes


def merge_nodes(tokenizer, bacterial_names, disease_names, nutrient_names, food_names, parser_output):
    entities_names = ['BACTERIUM', 'NUTRIENT', 'DISEASE', 'FOOD']
    names_lists = [bacterial_names, nutrient_names, disease_names, food_names]

    for entity_name, names_list in zip(entities_names, names_lists):
        for name in names_list:
            tokenized_sentence = [parser_output.words[i] for i in sorted(parser_output.words.keys())]
            tokenized_sentence_ids = sorted(parser_output.words.keys())

            name_tokens = tokenizer.tokenize(name)
            tokens_ids_ranges = []
            for i in range(len(tokenized_sentence) - len(name_tokens) + 1):
                if name_tokens == tokenized_sentence[i:i + len(name_tokens)]:
                    tokens_ids_ranges.append(tokenized_sentence_ids[i:i + len(name_tokens)])

            for _range in tokens_ids_ranges:
                merged_id = min(_range)
                for i, j in parser_output.nx_graph.edges()[:]:
                    rel = parser_output.nx_graph[i][j]['rel']
                    if i in _range and j in _range:
                        parser_output.nx_graph.remove_edge(i, j)
                    elif i in _range:
                        parser_output.nx_graph.remove_edge(i, j)
                        parser_output.nx_graph.add_edge(merged_id, j, {'rel': rel})
                    elif j in _range:
                        parser_output.nx_graph.remove_edge(i, j)
                        parser_output.nx_graph.add_edge(i, merged_id, {'rel': rel})
                parser_output.nx_graph.remove_nodes_from([_id for _id in _range if _id != merged_id])
                parser_output.words[merged_id] = name
                parser_output.tags[merged_id] = entity_name

                for _id in _range:
                    if _id != merged_id:
                        del parser_output.words[_id]
                        del parser_output.tags[_id]


def get_tokenizer(self):
    return self.__tokenizer
