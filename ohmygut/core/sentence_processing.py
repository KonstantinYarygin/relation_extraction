# -*- coding: utf-8 -*-
import abc
import matplotlib.pyplot as plt
import networkx as nx
import re

import spacy


class SentenceParser(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def parse_sentence(self, sentence, entities):
        raise NotImplementedError("Method have to be implemented")


class SpacySentenceParser(SentenceParser):
    def __init__(self):
        self.nlp = spacy.load('en')

    def parse_sentence(self, sentence, entities):
        tokens = self.nlp(sentence)
        edges = []
        words = {token.i: token.orth_ for token in tokens}
        tags = {token.i: token.tag_ for token in tokens}
        indexes = []
        # replacing tags with BACTERIA, NUTRIENT, etc.
        for i, entity in enumerate(entities):
            for j, word in words.items():
                if entity.name == word:
                    index = (j, i)
                    if index not in indexes:
                        indexes.append(index)
        for token_index, entity_index in indexes:
            tags[token_index] = entities[entity_index].tag

        for token in tokens:
            edges.append((token.i, token.head.i, {'rel': token.dep_}))

        nx_graph = nx.DiGraph()
        nx_graph.add_nodes_from(words.keys())
        nx_graph.add_edges_from(edges)
        parser_output = ParserOutput(sentence, nx_graph, words, tags)
        return parser_output


class StanfordSentenceParser(SentenceParser):
    def __init__(self, stanford_dependency_parser, stanford_tokenizer):
        self.stanford_dependency_parser = stanford_dependency_parser
        self.stanford_tokenizer = stanford_tokenizer

    def parse_sentence(self, sentence, entities):
        try:
            dependency_graph_iterator = self.stanford_dependency_parser.raw_parse(sentence)
        except OSError:
            return

        dependency_graph = next(dependency_graph_iterator)
        tokens = self.stanford_tokenizer.tokenize(sentence)

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

        return ParserOutput(text=sentence,
                            nx_graph=nx_graph,
                            words=words,
                            tags=tags)


class ParserOutput(object):
    def __init__(self, text, nx_graph, words, tags):
        self.text = text
        self.nx_graph = nx_graph
        self.words = words
        self.tags = tags

    def draw(self, path_to_save=None):
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
        if not path_to_save:
            plt.show()
        else:
            plt.savefig(path_to_save, dpi=300)

    def __str__(self):
        object_string = ''
        object_string += str(self.nx_graph.adj) + '\n'
        object_string += str(self.words) + '\n'
        object_string += str(self.tags) + '\n'
        return(object_string)
