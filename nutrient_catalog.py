from nltk.tokenize import word_tokenize

class NutrientCatalog(object):
    """docstring for NutrientCatalog"""
    def __init__(self):
        fatty_acids = []
        with open('./data/nutrients/unsaturated_fatty_acids.list.txt') as usfa, \
             open('./data/nutrients/saturated_fatty_acids.list.txt') as sfa, \
             open('./data/nutrients/other_acids.list.txt') as other:
            fatty_acids.extend(usfa.readlines())
            fatty_acids.extend(sfa.readlines())
            fatty_acids.extend(other.readlines())
        fatty_acids = [acid.strip() for acid in fatty_acids]
        fatty_acids = [acid.split()[0] for acid in fatty_acids]
        fatty_acids_low = [acid[0].lower() + acid[1:] for acid in fatty_acids]
        fatty_acids_upp = [acid[0].upper() + acid[1:] for acid in fatty_acids]
        fatty_acids = fatty_acids_upp + \
                      fatty_acids_low + \
                      ['iso'+acid for acid in fatty_acids_low] + \
                      ['iso-'+acid for acid in fatty_acids_low] + \
                      ['Iso'+acid for acid in fatty_acids_low] + \
                      ['Iso-'+acid for acid in fatty_acids_low]
        self.fatty_acids = {acid: True for acid in fatty_acids}
    def find_nutrient(self, text):
        list_text = word_tokenize(text)
        nutrients_list = [word for word in list_text if word in self.fatty_acids]
        return(nutrients_list)
