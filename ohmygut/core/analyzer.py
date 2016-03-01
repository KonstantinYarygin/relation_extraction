from itertools import product
import networkx as nx

class SentenceAnalyzer(object):
    def __init__(self, stemmer, tokenizer):
        self.__stemmer = stemmer
        self.__tokenizer = tokenizer

    def analyze(self, sentence):
        self.merge_nodes(sentence)
        bacteria_nodes_ids = [id for id, tag in sentence.parse_result.tags.items() if tag == 'BACTERIUM']
        nutrients_nodes_ids = [id for id, tag in sentence.parse_result.tags.items() if tag == 'NUTRIENT']
        diseases_nodes_ids = [id for id, tag in sentence.parse_result.tags.items() if tag == 'DISEASE']
        pathes = []
        for bacterium_node_id, nutrient_node_id in product(bacteria_nodes_ids, nutrients_nodes_ids):
            pathes.append(self.search_path(sentence, bacterium_node_id, nutrient_node_id))

        return(pathes)
        
    def merge_nodes(self, sentence):
        bacterial_names = [name for name, ncbi_id in sentence.bacteria]
        disease_names = [name for name, doid_id in sentence.diseases]
        nutrient_names = [name for name, idname in sentence.nutrients]
        entities_list = ['BACTERIUM', 'NUTRIENT', 'DISEASE']

        for entity_name, names_list in zip(entities_list, [bacterial_names, nutrient_names, disease_names]):
            for name in names_list:
                # tokens = self.__tokenizer.tokenize(name)
                tokens = name.split(' ')
                if len(tokens) > 1:
                    tokens_ids = []
                    for token in tokens:
                        index = list(sentence.parse_result.words.values()).index(token)
                        tokens_ids.append(list(sentence.parse_result.words.keys())[index])
                    merged_id = min(tokens_ids)
                    for i, j in sentence.parse_result.nx_graph.edges()[:]:
                        if i in tokens_ids and j in tokens_ids:
                            sentence.parse_result.nx_graph.remove_edge(i, j)
                        elif i in tokens_ids:
                            rel = sentence.parse_result.nx_graph[i][j]['rel']
                            sentence.parse_result.nx_graph.remove_edge(i, j)
                            sentence.parse_result.nx_graph.add_edge(merged_id, j, {'rel': rel})
                        elif j in tokens_ids:
                            rel = sentence.parse_result.nx_graph[i][j]['rel']
                            sentence.parse_result.nx_graph.remove_edge(i, j)
                            sentence.parse_result.nx_graph.add_edge(i, merged_id, {'rel': rel})
                    sentence.parse_result.nx_graph.remove_nodes_from([id for id in tokens_ids if id != merged_id])
                    sentence.parse_result.words[merged_id] = name
                    sentence.parse_result.tags[merged_id] = entity_name
                    for id in tokens_ids:
                        if id != merged_id:
                            del sentence.parse_result.words[id]
                            del sentence.parse_result.tags[id]
                else:
                    index = list(sentence.parse_result.words.values()).index(name)
                    id = list(sentence.parse_result.words.keys())[index]
                    sentence.parse_result.tags[id] = entity_name

    def search_path(self, sentence, source, target, undirected=True):

        if undirected:
            G = sentence.parse_result.nx_graph.to_undirected()
        else:
            G = sentence.parse_result.nx_graph

        try:
            pos_path = nx.dijkstra_path(G, source, target)
        except nx.exception.NetworkXNoPath:
            return {}

        edge_rels = [G[i][j]['rel'] for i, j in zip(pos_path[:-1], pos_path[1:])]
        words = [sentence.parse_result.words[i] for i in pos_path]
        tags = [sentence.parse_result.tags[i] for i in pos_path]
        return {'edge_rels': edge_rels, 'words': words, 'tags': tags, 'pos_path': pos_path}


    def find_patterns(self, path, additional_graph):
        pass
