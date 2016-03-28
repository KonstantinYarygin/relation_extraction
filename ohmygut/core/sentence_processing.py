# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import networkx as nx
import re


class SentenceParser(object):
    def __init__(self, stanford_dependency_parser, stanford_tokenizer):
        self.stanford_dependency_parser = stanford_dependency_parser
        self.stanford_tokenizer = stanford_tokenizer

    def parse_sentence(self, sentence):
        try:
            dependency_graph_iterator = self.stanford_dependency_parser.raw_parse(sentence)
        except OSError:
            return

        dependency_graph = next(dependency_graph_iterator)
        tokens = self.stanford_tokenizer.tokenize(sentence)

        # nodes = [node for node in dependency_graph.nodes.keys() if node]
        nodes = [i+1 for i in range(len(tokens))]
        edges = [
            (n, dependency_graph._hd(n), {'rel': dependency_graph._rel(n)})
            for n in dependency_graph.nodes if n and dependency_graph._hd(n)
            ]

        nx_graph = nx.DiGraph()
        nx_graph.add_nodes_from(nodes)
        nx_graph.add_edges_from(edges)

        words = {i+1: token for i, token in enumerate(tokens)}
        tags = {node: dependency_graph.nodes[node]['tag'] if node in dependency_graph.nodes else 'NO_TAG' for node in nodes}

        return ParserOutput(nx_graph=nx_graph,
                            words=words,
                            tags=tags)


class ParserOutput(object):
    def __init__(self, nx_graph, words, tags):
        self.nx_graph = nx_graph
        self.words = words
        self.tags = tags

    def draw(self):
        G = self.nx_graph.to_undirected()
        pos = nx.spring_layout(G)

        nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='white')
        nx.draw_networkx_edges(G, pos, width=6, alpha=0.5, edge_color='black')
        nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif',
                                labels=self.words
                                )
        nx.draw_networkx_edge_labels(G, pos, font_size=10,
                                     edge_labels=dict(((i, j), G[i][j]['rel']) for i, j in G.edges())
                                     )
        plt.axis('off')
        plt.show()

    def __str__(self):
        object_string = ''
        object_string += str(self.nx_graph.edges()) + '\n'
        object_string += str(self.words) + '\n'
        object_string += str(self.tags) + '\n'
        return(object_string)
