# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import networkx as nx
import re


def trim_sentence(sent):
    patterns = ['\[\s?\d+[(and)\-,\d\s]*\]',
                '\[20\d\d\w?\]',
                '\[19\d\d\w?\]',
                '\[(supplementary|supp|supp\.|suppl|suppl\.)?\s?(table|tables|tbl|tbl\.)\s?[Ss]?\d+([(and)\-,\sS\d]*)?\]',
                '\[(supplementary|supp|supp\.|suppl|suppl\.)?\s?(figure|figures|fig|fig\.)\s?[Ss]?\d+([(and)\-,\sS\d]*)?\]',
                '\[(supplementary|supp|supp\.|suppl|suppl\.)?\s?(data)\s?[Ss]?\d+([(and)\-,\sS\d]*)?\]'
                '\(\s?\d+[(and)\-,\d\s]*\)',
                '\(20\d\d\w?\)',
                '\(19\d\d\w?\)',
                '\((supplementary|supp|supp\.|suppl|suppl\.)?\s?(table|tables|tbl|tbl\.)\s?[Ss]?\d+([(and)\-,\sS\d]*)?\)',
                '\((supplementary|supp|supp\.|suppl|suppl\.)?\s?(figure|figures|fig|fig\.)\s?[Ss]?\d+([(and)\-,\sS\d]*)?\)',
                '\((supplemental|supp|supp\.|suppl|suppl\.)?\s?(data)\s?[Ss]?\d+([(and)\-,\sS\d]*)?\)']
    match_lists = [re.finditer(pattern, sent, re.IGNORECASE) for pattern in patterns]
    substrings = [match.group() for match_list in match_lists for match in match_list if match]
    out_sent = sent
    for substring in substrings:
        out_sent = out_sent.replace(substring, '')
    return (out_sent)


class SentenceParser(object):
    """docstring for SentenceParser"""

    def __init__(self, stanford_dependency_parser):
        self.stanford_dependency_parser = stanford_dependency_parser

    def parse_sentence(self, sentence):
        sentence_trimmed = trim_sentence(sentence)
        dependency_graph_iterator = self.stanford_dependency_parser.raw_parse(sentence_trimmed)
        dependency_graph = next(dependency_graph_iterator)

        nodes = [node for node in dependency_graph.nodes.keys() if node]
        edges = [
            (n, dependency_graph._hd(n), {'rel': dependency_graph._rel(n)})
            for n in nodes if dependency_graph._hd(n)
            ]

        nx_graph = nx.DiGraph()
        nx_graph.add_nodes_from(nodes)
        nx_graph.add_edges_from(edges)

        words = {node: dependency_graph.nodes[node]['word'] for node in nodes}
        tags = {node: dependency_graph.nodes[node]['tag'] for node in nodes}

        return ParserOutput(nx_graph=nx_graph,
                            words=words,
                            tags=tags)


class ParserOutput(object):
    """docstring for SentenceGraph"""

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
