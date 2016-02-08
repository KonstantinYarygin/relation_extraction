import matplotlib.pyplot as plt
import networkx as nx
import os
import re

from stanford_wrapper import parse_dependencies
from itertools import product
from nltk import pos_tag


class SentGraph(nx.DiGraph):
    """docstring for SentGraph"""
    def __init__(self):
        nx.DiGraph.__init__(self)

    def search_path(self, source, target, undirected=True):
        if undirected:
            G = self.to_undirected()
        else:
            G = self

        try:
            pos_path = nx.dijkstra_path(G, source, target)
        except nx.exception.NetworkXNoPath:
            return({})

        path_edges = [G[i][j]['type'] for i, j in zip(pos_path[:-1], pos_path[1:])]
        return({'pos_path': pos_path, 'path_edges': path_edges})

    def remove_conj_edges(self):
        for i, j in self.edges():
            if self[i][j]['type'].startswith('conj') or \
               self[i][j]['type'] == 'advcl':
                self.remove_edge(i, j)

    def draw(self):
        G = self.to_undirected()
        # G = self
        pos = nx.spring_layout(G)

        nx.draw_networkx_nodes(G, pos, node_size=1000, node_color="white")
        nx.draw_networkx_edges(G, pos, width=6, alpha=0.5, edge_color='black')
        nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif',
                                labels=dict([(k, G.node[k]['word']) for k in G.nodes()])
                                )
        nx.draw_networkx_edge_labels(G,pos, font_size=10, 
                                edge_labels=dict([((i, j), G[i][j]['type'])for i, j in G.edges()])
                                )
        plt.axis('off')
        plt.show()

class SentenceProcessor(object):
    """docstring for SentenceProcessor"""
    def __init__(self, sentence, parser_output):

        self.sentence = sentence

        # self.sentence = self.trim_sentence(sentence)
        # parser_output = parse_dependencies(self.sentence)
        # print(parser_output['graph_raw'])

        self.tokens = ['ROOT'] + parser_output['tokenized_sent']
        self.tags = ['ROOT'] + [x[1] for x in pos_tag(self.tokens[1:])]
        self.positions = range(0, len(self.tokens) + 1)
        self.pos_token_tag = zip(self.positions, self.tokens, self.tags)

        self.pos_to_word = dict(zip(self.positions, self.tokens))
        self.pos_to_tag = dict(zip(self.positions, self.tags))

        self.word_to_pos = {word: [] for word in self.tokens}
        [self.word_to_pos[word].append(pos) for pos, word in self.pos_to_word.items()]

        if parser_output['graph_raw']:
            self.deploy_graph(parser_output['graph_raw'])

    def __repr__(self):
        out = self.sentence + '\n'
        out += '\n'.join(map(str, self.pos_token_tag))
        return(out)

    def trim_sentence(self, sent):
        patterns = ['\[\s?\d+[(and)\-,\d\s]*\]',
                    '\[20\d\d\w?\]',
                    '\[19\d\d\w?\]',
                    '\[(supplementary|supp|supp\.|suppl|suppl\.)?\s?(table|tables|tbl|tbl\.)\s?[Ss]?\d+([(and)\-,\sS\d]*)?\]',
                    '\[(supplementary|supp|supp\.|suppl|suppl\.)?\s?(figure|figures|fig|gif\.)\s?[Ss]?\d+([(and)\-,\sS\d]*)?\]',
                    '\[(supplementary|supp|supp\.|suppl|suppl\.)?\s?(data)\s?[Ss]?\d+([(and)\-,\sS\d]*)?\]',
                    '\(\s?\d+[(and)\-,\d\s]*\)',
                    '\(20\d\d\w?\)',
                    '\(19\d\d\w?\)',
                    '\((supplementary|supp|supp\.|suppl|suppl\.)?\s?(table|tables|tbl|tbl\.)\s?[Ss]?\d+([(and)\-,\sS\d]*)?\)',
                    '\((supplementary|supp|supp\.|suppl|suppl\.)?\s?(figure|figures|fig|gif\.)\s?[Ss]?\d+([(and)\-,\sS\d]*)?\)',
                    '\((supplementary|supp|supp\.|suppl|suppl\.)?\s?(data)\s?[Ss]?\d+([(and)\-,\sS\d]*)?\)']
        match_lists = [re.finditer(pattern, sent, re.IGNORECASE) for pattern in patterns]
        substrings = [match.group() for match_list in match_lists for match in match_list if match]
        out_sent = sent
        for substring in substrings:
            out_sent = out_sent.replace(substring, '')
        return(out_sent)

    def deploy_graph(self, graph_raw):
        self.Graph = SentGraph()

        for line in graph_raw:
            m = re.match('^(.+)\((.+)-(\d+),\s(.+)-(\d+)\)$', line)
            if not m:
                continue
            edge_type, word_1, pos_1, word_2, pos_2 = [m.group(x) for x in range(1, 6)]
            pos_1 = int(pos_1)
            pos_2 = int(pos_2)

            self.Graph.add_node(pos_1, {'word': word_1,
                                        'tag': self.pos_to_tag[pos_1]})
            self.Graph.add_node(pos_2, {'word': word_2,
                                        'tag': self.pos_to_tag[pos_2]})

            self.Graph.add_edge(pos_1, pos_2, {'type': edge_type})
        # self.Graph.draw()
        self.Graph.remove_conj_edges()

    def search_path(self, word_1, word_2):
        source_pos = self.word_to_pos[word_1][0]
        target_pos = self.word_to_pos[word_2][0]
        out = self.Graph.search_path(source_pos, target_pos)
        if out:
            out['path'] = [self.pos_to_word[pos] for pos in out['pos_path']]
            out['tags'] = [self.pos_to_tag[pos] for pos in out['pos_path']]
        return(out)


# sent = 'A cellulolytic bacterium that showed 99% 16S rDNA sequence similarity to M.-oxydans has been found to produce an array of cellulolytic-xylanolytic enzymes (filter paper cellulase, alpha-glucosidase, xylanase , and beta-xylosidase)[52].'
# sent = 'B.-barnesiae does not utilize mannitol, arabinose, glycerol, melezitose, sorbitol, rhamnose or trehalose[1].'
# sent = 'Protozoa are important hydrogen-producers within the rumen while the methanogenic Archaea utilize the hydrogen for methane production [16],[26].'
# sent = 'D.-vulgaris typically uses lactate as a substrate and secretes a mixture of formate, hydrogen, acetate and CO2 in the absence of sulfate, while M.-maripaludis consumes acetate, hydrogen and CO2 to produce methane.'
# # sent = 'Increased Enterobacteriaceae numbers were related to increased ferritin and reduced transferrin , while Bacteroides numbers were related to increased HDL-cholesterol and folic acid levels [Santacruz et al. , 2010 ; Table 1].'
# sent = 'Increased Enterobacteriaceae numbers were related to increased ferritin and reduced transferrin , while Bacteroides numbers were related to increased HDL-cholesterol and folic acid levels [Table 1].'
# sent = 'No or weak propionic utilisation was seen in all C.-jejuni strains tested while strong propionic utilisation was seen for all C.-coli strains tested.'
# sp = SentenceProcessor(sent, {})
# print(' '.join(sp.tokens))
# print(' '.join(sp.tags))
# # sp.Graph.draw()
# # print([sp.Graph.to_undirected()[node] for node in sp.Graph.nodes()])
# # edge_types = [x['type'] for x in sp.Graph[sp.word_to_pos['utilize'][0]].values()]
# # print(edge_types)

# No or weak propionic utilisation was seen in all C.-jejuni strains tested while strong propionic utilisation was seen for all C.-coli strains tested .
# DT CC JJ JJ NN VBD VBN IN DT NNP NNS VBD IN JJ JJ NN VBD VBN IN PDT NNP NNS VBD .
