import re

# Например:
# Имена болезней:
#
#   squamous cell carcinoma
#   squamous carcinoma
#   squamous cell cancer
#   squamous cell carcinoma (disorder)
#   squamous cell carcinoma (morphologic abnormality)
#   squamous cell carcinoma NOS (morphologic abnormality)
#
#
# Структура дерева:
#
#            |-- carcinoma*              |-- (disorder)*
# squamous --|                           |
#            |-- cell --|-- carcinoma* --|-- (morphologic -- abnormality)*
#                       |                |
#                       |-- cancer*      |-- NOS -- (morphologic -- abnormality)*
#
# символ * означает конец какого-либо названия болезни

class w_tree_node(object):
    def __init__(self):
        self.is_end = False
        self.children = {}

class DiseaseOntology(object):
    def __init__(self, path='./data/diseases/HumanDO.obo'):
        with open(path) as f:
            data = [[]] 
            for line in f.readlines():
                if line == '\n':
                    data.append([])
                else:
                    data[-1].append(line.strip())
        
        # из онтологии берем id и названия болезней с синонимами
        data = [item for item in data if (item != [] and item[0] == '[Term]')]

        self.disease_by_DOID = {} #key - DOID; value - disease names
        for item in data:
            item_DOID = ''
            for line in item:
                if line.startswith('id:'):
                    match = re.match('^id: DOID:(\d+)', line)
                    item_DOID = match.group(1).strip()
                    self.disease_by_DOID[item_DOID] = []
                    continue
                if line.startswith('name:'):
                    match = re.match('^name: (.*)', line)
                    disease_name = match.group(1).strip()
                    self.disease_by_DOID[item_DOID].append(disease_name)
                    continue
                if line.startswith('synonym:'):
                    match = re.match('^synonym: \"(.*)\".*', line)
                    disease_name = match.group(1).strip()
                    self.disease_by_DOID[item_DOID].append(disease_name)
                    continue

        self.diseases = {} #key - disease name; value - DOID
        for DOID in self.disease_by_DOID:
            for disease in self.disease_by_DOID[DOID]:
                self.diseases[disease] = DOID
                if disease[0].islower():
                    self.diseases[disease[0].upper() + disease[1:]] = DOID

        # строим дерево с названиями всех болезней
        self.root = w_tree_node()

        for disease in self.diseases.keys():
            disease_list = disease.split()
            cur_node = self.root
            for i, word in enumerate(disease_list):
                if not(word in cur_node.children):
                    cur_node.children[word] = w_tree_node()
                cur_node = cur_node.children[word]
                if (i == len(disease_list) - 1):
                    cur_node.is_end = True

    def find_disease(self, text):
        # ищем имена из онтологии и подсчитываем количества упоминаний (учитывая синонимы)

        text = text.strip()
        text = text.split()
        text = [x.strip('.,()[]1234567890 ') for x in text]
        text = [x for x in text if x]

        diseases_in_text = []
        for i, word in enumerate(text):
            if word in self.root.children:
                cur_node = self.root.children[word]
                flag = True
                j = i
                while flag:
                    if cur_node.is_end:
                        diseases_in_text.append(text[i:j + 1])
                    if j >= len(text) - 1:
                        break
                    j += 1
                    flag = False
                    if text[j] in cur_node.children:
                        cur_node = cur_node.children[text[j]]
                        flag = True

        diseases_in_text = [' '.join(disease) for disease in diseases_in_text]
        DOIDs_list = [self.diseases[disease] for disease in diseases_in_text]

        DOIDs_count = {}
        for DOID in DOIDs_list:
            if not(DOID in DOIDs_count):
                DOIDs_count[DOID] = 0
            DOIDs_count[DOID] += 1

        return_list = []
        for DOID in DOIDs_count:
            return_list.append((DOIDs_count[DOID],
                        'DOID:%s' % DOID,
                        self.disease_by_DOID[DOID][0]))
            
        return_list = sorted(return_list, key=lambda x: x[0], reverse=True)

        return return_list

# DO = DiseaseOntology()
# print(DO.find_disease('cancer ahahahah lung cancer'))