
def parse_abstracts(path):
    tree = etree.parse(path)
    root = tree.getroot()
    articles_list = []
    for element in root.iter(tag=etree.Element):
        # print("%s - %s" % (element.tag, element.text))
        if element.tag == 'MedlineCitation':
            article = Article()
            for child in element:
                if child.tag == 'PMID':
                    article.PMID = child.text
                if child.tag == 'Article':
                    for sub_article in child:
                        if sub_article.tag == 'ArticleTitle':
                            article.title = sub_article.text
                        if sub_article.tag == 'Abstract':
                            for sub_element in sub_article:
                                if sub_element.tag == 'AbstractText':
                                    if sub_element.text is not None:
                                        article.abstract += sub_element.text
                        if sub_article.tag == 'AuthorList':
                            for sub_author in sub_article:
                                last_name = ''
                                for author in sub_author:
                                    if author.tag == 'LastName':
                                        last_name = author.text
                                    elif author.tag == 'Initials':
                                        article.authors.append(' '.join((last_name, author.text)))
                    articles_list.append(article)
    return articles_list

# =========================================================================== #
# =========================================================================== #

fatty_acids = []
with open('./data/nutrients/unsaturated_fatty_acids.list.txt') as usfa, \
     open('./data/nutrients/saturated_fatty_acids.list.txt') as sfa:
    fatty_acids.extend(usfa.readlines())
    fatty_acids.extend(sfa.readlines())
fatty_acids = [acid.strip() for acid in fatty_acids]
fatty_acids = [acid.split()[0] for acid in fatty_acids]
fatty_acids = [acid.lower() for acid in fatty_acids]
fatty_acids = fatty_acids + ['iso'+acid for acid in fatty_acids]
fatty_acids = {acid: True for acid in fatty_acids}

# =========================================================================== #
# =========================================================================== #


class TreeNode(object):
    def __init__(self):
        self.is_end = False
        self.children = {}

def plural(word):
    # latin
    if word.endswith('a'):
        return(word[:-1] + 'ae')
    elif word.endswith('en'):
        return(word[:-2] + 'ina')
    elif word.endswith('ex'):
        return(word[:-2] + 'ices')
    elif word.endswith('itis'):
        return(word[:-4] + 'itides')
    elif word.endswith('is'):
        return(word[:-2] + 'es')
    elif word.endswith('ix'):
        return(word[:-2] + 'ices')
    elif word.endswith('on'):
        return(word[:-2] + 'a')
    elif word.endswith('um'):
        return(word[:-2] + 'a')
    elif word.endswith('us'):
        return(word[:-2] + 'i')
    else:
        return(word + 'i')
    # english
    # elif word.endswith('y'):
    #     return(word[:-1] + 'ies')
    # elif word[-1] in 'sx' or word[-2:] in ['sh', 'ch']:
    #     return(word + 'es')
    # elif word.endswith('an'):
    #     return(word[:-2] + 'en')
    # else:
    #     return(word + 's')


class BacteriaCatalog(object):
    def __init__(self, path='./data/bacteria/taxonomy_table.tsv'):
        with open(path) as f:
            data = f.readlines()[1:]
            data = [line.strip('\n').split('\t')[5:-1] for line in data]
        
        for i, record in enumerate(data):
            species_name = record[0].split(maxsplit=1)
            genus_name = record[1]
            plural_genus_name = plural(genus_name)
            data[i].append(plural_genus_name)
            data[i].append(genus_name + ' sp.')
            data[i].append(genus_name + ' sp')
            data[i].append(plural_genus_name + ' spp.')
            data[i].append(plural_genus_name + ' spp')
            data[i].append(species_name[0][0] + '. ' + species_name[1])

        self.root = TreeNode()
        # sdelat' - do maksimal'noy glubiny, ne zapisyvat' vsio na puti, tol'ko maximal'no vozmozhnoye
        for record in data[:]:
            for name_line in record:
                if not name_line or name_line == 'NA':
                    continue
                name_list = [word.lower() for word in name_line.split(' ')]
                cur_node = self.root
                for i, word in enumerate(name_list):
                    if not(word in cur_node.children):
                        cur_node.children[word] = TreeNode()
                    cur_node = cur_node.children[word]
                    if (i == len(name_list) - 1):
                        cur_node.is_end = True
    
    def find_bacteria(self, text):

        text = word_tokenize(text)
        low_text = [word.lower() for word in text]
        # print(low_text)

        bacteria_in_text = []
        for i, word in enumerate(low_text):
            if word in self.root.children:
                cur_node = self.root.children[word]
                flag = True
                j = i
                while flag:
                    if cur_node.is_end:
                        bacteria_in_text.append([i, j])
                    if j >= len(low_text) - 1:
                        break
                    j += 1
                    flag = False
                    if low_text[j] in cur_node.children:
                        cur_node = cur_node.children[low_text[j]]
                        flag = True
        bacteria_in_text = [text[i:j+1] for i, j in bacteria_in_text]
        bacteria_in_text = [' '.join(bacteria) for bacteria in bacteria_in_text]
        bacteria_in_text = list(set(bacteria_in_text))
        return(bacteria_in_text)

BC = BacteriaCatalog()

# =========================================================================== #
# =========================================================================== #

# sentence_graph = sentence_graph_creator.get_sentence_graph(sentence)
# sentence = 'B.-barnesiae does not utilize mannitol, arabinose, glycerol, melezitose, sorbitol, rhamnose or trehalose.'

# sent = 'A cellulolytic bacterium that showed 99% 16S rDNA sequence similarity to M.-oxydans has been found to produce an array of cellulolytic-xylanolytic enzymes (filter paper cellulase, alpha-glucosidase, xylanase , and beta-xylosidase)[52].'
# sent = 'Protozoa are important hydrogen-producers within the rumen while the methanogenic Archaea utilize the hydrogen for methane production [16],[26].'
# sent = 'B.-barnesiae does not utilize mannitol, arabinose, glycerol, melezitose, sorbitol, rhamnose or trehalose[1].'
# sent = 'D.-vulgaris typically uses lactate as a substrate and secretes a mixture of formate, hydrogen, acetate and CO2 in the absence of sulfate, while M.-maripaludis consumes acetate, hydrogen and CO2 to produce methane.'
# # sent = 'Increased Enterobacteriaceae numbers were related to increased ferritin and reduced transferrin , while Bacteroides numbers were related to increased HDL-cholesterol and folic acid levels [Santacruz et al. , 2010 ; Table 1].'
# sent = 'Increased Enterobacteriaceae numbers were related to increased ferritin and reduced transferrin , while Bacteroides numbers were related to increased HDL-cholesterol and folic acid levels [Table 1].'
# sent = 'No or weak propionic utilisation was seen in all C.-jejuni strains tested while strong propionic utilisation was seen for all C.-coli strains tested.'
# sp = SentenceGraphCreator(sent, {})
# print(' '.join(sp.tokens))
# print(' '.join(sp.tags))
# # sp.Graph.draw()
# # print([sp.Graph.to_undirected()[node] for node in sp.Graph.nodes()])
# # edge_types = [x['type'] for x in sp.Graph[sp.word_to_pos['utilize'][0]].values()]
# # print(edge_types)

# DT CC JJ JJ NN VBD VBN IN DT NNP NNS VBD IN JJ JJ NN VBD VBN IN PDT NNP NNS VBD .

# =========================================================================== #
# =========================================================================== #

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

def remove_conj_edges(self):
    for i, j in self.edges():
        if self[i][j]['type'].startswith('conj') or \
                        self[i][j]['type'] == 'advcl':
            self.remove_edge(i, j)

# =========================================================================== #
# =========================================================================== #
