from hash_tree import HashTree

class NutrientsCatalog(object):
    """Object holding nutrient ontology"""
    def __init__(self, path='./data/nutrients/natalia_nitrients.txt',
                       verbose=True):
        if verbose:
            print('Creating nutrients catalog...')

        with open(path) as nn:
            lines = [line.strip() for line in nn.readlines()]
            lines = [line for line in lines if line]
        nutrients_low = [line[0].lower() + line[1:] for line in lines]
        nutrients_upp = [line[0].upper() + line[1:] for line in lines]
        nutrients = nutrients_upp + nutrients_low
        nutrients = [nutr[:-5] if nutr.endswith(' acid') else nutr for nutr in nutrients]

        self.nutrients = {nutrient: True for nutrient in nutrients}
    
        self.hash_tree = HashTree(self.nutrients.keys())

    def find(self, text):
        """ Uses previously generated hash tree to search text for nutrient names

        input:
            text: text to search for nutrient names

        returns:
            list of nutrient_names
        """
        nutr_names = self.hash_tree.search(text)
        return(nutr_names)


# class NutrientCatalog(object):
#     """docstring for NutrientCatalog"""
#     def __init__(self):
#         print('Creating nutrients catalog...')
        
#         fatty_acids = []
#         with open('./data/nutrients/unsaturated_fatty_acids.list.txt') as usfa, \
#              open('./data/nutrients/saturated_fatty_acids.list.txt') as sfa, \
#              open('./data/nutrients/other_acids.list.txt') as other:
#             fatty_acids.extend(usfa.readlines())
#             fatty_acids.extend(sfa.readlines())
#             fatty_acids.extend(other.readlines())
#         fatty_acids = [acid.strip() for acid in fatty_acids]
#         fatty_acids = [acid.split()[0] for acid in fatty_acids]
#         fatty_acids_low = [acid[0].lower() + acid[1:] for acid in fatty_acids]
#         fatty_acids_upp = [acid[0].upper() + acid[1:] for acid in fatty_acids]
#         fatty_acids = fatty_acids_upp + \
#                       fatty_acids_low + \
#                       ['iso'+acid for acid in fatty_acids_low] + \
#                       ['iso-'+acid for acid in fatty_acids_low] + \
#                       ['Iso'+acid for acid in fatty_acids_low] + \
#                       ['Iso-'+acid for acid in fatty_acids_low]
#         self.fatty_acids = {acid: True for acid in fatty_acids}

