from itertools import product
import networkx as nx

class ShortestPath():
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


def analyze_sentence(sentence, tokenizer, pattern_finder):
    bacterial_names = [name for name, ncbi_id in sentence.bacteria]
    disease_names = [name for name, doid_id in sentence.diseases]
    nutrient_names = [name for name, idname in sentence.nutrients]
    parser_output = sentence.parser_output

    merge_nodes(tokenizer, bacterial_names, disease_names, nutrient_names, parser_output)
    bacteria_nodes_ids = [id for id, tag in sentence.parser_output.tags.items() if tag == 'BACTERIUM']
    nutrients_nodes_ids = [id for id, tag in sentence.parser_output.tags.items() if tag == 'NUTRIENT']
    # diseases_nodes_ids = [id for id, tag in sentence.parser_output.tags.items() if tag == 'DISEASE']
    shortest_pathes = []
    for bacterium_node_id, nutrient_node_id in product(bacteria_nodes_ids, nutrients_nodes_ids):
        shortest_path = search_shortest_path(sentence, bacterium_node_id, nutrient_node_id)
        if not shortest_path:
            continue
        pattern_verbs = pattern_finder.find_patterns(shortest_path,
                                                     sentence.parser_output.nx_graph,
                                                     sentence.parser_output.words)
        if pattern_verbs:
            shortest_path.type = pattern_verbs

        shortest_pathes.append(shortest_path)

    return shortest_pathes


def merge_nodes(tokenizer, bacterial_names, disease_names, nutrient_names, parser_output):
    entities_list = ['BACTERIUM', 'NUTRIENT', 'DISEASE']

    for entity_name, names_list in zip(entities_list, [bacterial_names, nutrient_names, disease_names]):
        for name in names_list:
            tokens = tokenizer.tokenize(name)
            if len(tokens) > 1:
                tokens_ids = []
                for token in tokens:
                    index = list(parser_output.words.values()).index(token)
                    tokens_ids.append(list(parser_output.words.keys())[index])
                merged_id = min(tokens_ids)
                for i, j in parser_output.nx_graph.edges()[:]:
                    if i in tokens_ids and j in tokens_ids:
                        parser_output.nx_graph.remove_edge(i, j)
                    elif i in tokens_ids:
                        rel = parser_output.nx_graph[i][j]['rel']
                        parser_output.nx_graph.remove_edge(i, j)
                        parser_output.nx_graph.add_edge(merged_id, j, {'rel': rel})
                    elif j in tokens_ids:
                        rel = parser_output.nx_graph[i][j]['rel']
                        parser_output.nx_graph.remove_edge(i, j)
                        parser_output.nx_graph.add_edge(i, merged_id, {'rel': rel})
                parser_output.nx_graph.remove_nodes_from([id for id in tokens_ids if id != merged_id])
                parser_output.words[merged_id] = name
                parser_output.tags[merged_id] = entity_name
                for id in tokens_ids:
                    if id != merged_id:
                        del parser_output.words[id]
                        del parser_output.tags[id]
            else:
                index = list(parser_output.words.values()).index(name)
                id = list(parser_output.words.keys())[index]
                parser_output.tags[id] = entity_name


def get_tokenizer(self):
    return self.__tokenizer
