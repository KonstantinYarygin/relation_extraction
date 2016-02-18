from itertools import product
import networkx as nx

class SentenceAnalyzer(object):
    def __init__(self, stemmer, tokenizer):
        self.__stemmer = stemmer
        self.__tokenizer = tokenizer

    def analyze(self, sentence):
        print(sentence.text)
        print(sentence.diseases)
        print(sentence.nutrients)
        print(sentence.bacteria)
        # print(sentence.parse_result))

        self.merge_nodes(sentence)

    def merge_nodes(self, sentence):
        bacterial_names = [name for name, ncbi_id in sentence.bacteria]
        disease_names = [name for name, doid_id in sentence.diseases]
        nutrient_names = sentence.nutrients

        for entity_name, names_list in zip(['BACTERIA', 'NUTRIENT', 'DISEASE'], [bacterial_names, nutrient_names, disease_names]):
            for name in names_list:
                tokens = self.__tokenizer.tokenize(name)
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

    def search_path(self, source, target, undirected=True):

        if undirected:
            G = self.to_undirected()
        else:
            G = self

        try:
            pos_path = nx.dijkstra_path(G, source, target)
        except nx.exception.NetworkXNoPath:
            return ({})

        path_edges = [G[i][j]['type'] for i, j in zip(pos_path[:-1], pos_path[1:])]
        return ({'pos_path': pos_path, 'path_edges': path_edges})