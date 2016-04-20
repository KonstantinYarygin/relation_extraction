from nltk import StanfordTokenizer

from ohmygut.core.analyzer import analyze_sentence
from ohmygut.core.sentence_processing import SpacySentenceParser
from ohmygut.paths import stanford_jar_path

"""
A help script to plot sentence graph
TODO: make as command line utility?
"""

sentence = "B. vulgatus protects against Escherichia coli-induced colitis in gnotobiotic interleukin-2 deficient mice."
# sentence = "Intriguingly, others have previously reported that pediatric IBD patients " \
#            "have increased serum antibody titers against a TonB-dependent receptor from " \
#            "human commensal Bacteroides caccae named OmpW."


stanford_tokenizer = StanfordTokenizer(path_to_jar=stanford_jar_path)
parser = SpacySentenceParser()
parser_output = parser.parse_sentence(sentence)

analyze_output = analyze_sentence(bacterial_names=['B. vulgatus'], nutrient_names=[],
                                  disease_names=['colitis'], food_names=[],
                                  parser_output=parser_output, tokenizer=stanford_tokenizer,
                                  pattern_finder=None)
# analyze_output = analyze_sentence(bacterial_names=['Bacteroides caccae'], nutrient_names=[],
#                                   disease_names=['IBD'], food_names=[],
#                                   parser_output=parser_output, tokenizer=stanford_tokenizer,
#                                   pattern_finder=None)


print(analyze_output)

parser_output.draw("path.png")
