from article_data_loader import ArticleCatalog
from bacteria_catalog import BacteriaCatalog
from nutrient_catalog import NutrientCatalog
from stanford_wrapper import parse_dependencies
from itertools import product

AC = ArticleCatalog('../data/texts/')
BC = BacteriaCatalog(verbose=False)
NC = NutrientCatalog(verbose=False)

print('\t'.join(['title', 'sentence', 'organism', 'nutrient']))
for article in AC[:]:
    for sent in article.full_text:
        bc_out = BC.find_bacteria(sent)
        nc_out = NC.find_nutrient(sent)
        if bc_out and nc_out:
            bact_list = list(set(b_rec[0].lower() for b_rec in bc_out))
            nutr_list = list(set(n.lower() for n in nc_out))
            for bact, nutr in product(bact_list, nutr_list):
                print('\t'.join([article.title[0], sent, bact, nutr]))
            # sent_x = sent

            # nutr_list = list(nc_out)
            # nutr_list_x = [nutr.replace(' ', '-') for nutr in nutr_list]
            # for nutr, nutr_x in zip(nutr_list, nutr_list_x):
            #     sent_x = sent_x.replace(nutr, nutr_x) # smth wrong here
            
            # bact_list = list(set([x[0] for x in bc_out]))
            # bact_list_x = [bact.replace(' ', '-') for bact in bact_list]
            # for bact, bact_x in zip(bact_list, bact_list_x):
            #     sent_x = sent_x.replace(bact, bact_x) # smth wrong here

            # po = parse_dependencies(sent_x)
            # if po:
            #     graph_raw = po['graph_raw']
            #     tokenized_sent = po['tokenized_sent']
            #     print(''.join(article.title).replace('\n', ' '))
            #     print('\t'.join(tokenized_sent))
            #     print('\t'.join(bact_list_x))
            #     print('\t'.join(nutr_list_x))
            #     print('\t'.join(graph_raw))
            #     print()
