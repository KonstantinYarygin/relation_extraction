import networkx
from nltk.parse.stanford import StanfordDependencyParser

parser = StanfordDependencyParser(
    path_to_jar='/home/anatoly/do/relation_extraction/stanford_parser/stanford-parser.jar',
    path_to_models_jar='/home/anatoly/do/relation_extraction/stanford_parser/stanford-parser-3.5.2-models.jar',
    model_path='/home/anatoly/do/relation_extraction/stanford_parser/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz'
)


def rel(self, i):
    try:
        return self.nodes[i]['rel']
    except IndexError:
        return None


def hd(self, i):
    try:
        return self.nodes[i]['head']
    except IndexError:
        return None


sentence = 'I am good and nice robot'
result = parser.raw_parse(sentence)
for a in result:
    # graph = a.nx_graph()
    nodes = list(range(1, len(a.nodes)))
    edges = [
        (n, hd(a, n), dict(rel=rel(a, n)))
        for n in a.nodes if hd(a, n)
        ]

    g = networkx.MultiDiGraph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)

print(g)
# edges = [(1, 4, {'type': 'nsubj'}),
#          (2, 4, {'type': 'cop'}),
#          (3, 4, {'type': 'amod'})]
# nodes = [1, 2, 3, 4]
