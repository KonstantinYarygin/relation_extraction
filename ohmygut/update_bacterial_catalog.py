from ohmygut.core.catalog.gut_bacteria_catalog import GutBacteriaCatalog

gut_bact_cat_path = '../data/bacteria/gut_catalog.csv'
gut_bact_list_path = '../data/bacteria/taxonomy_HMP_2013_NR_fixed.txt'

names_path = '../data/bacteria/taxdump/names.dmp'
nodes_path = '../data/bacteria/taxdump/nodes.dmp'

gut_bact_cat = GutBacteriaCatalog(gut_bact_cat_path)
gut_bact_cat.update(nodes_ncbi_path=nodes_path, names_ncbi_path=names_path,
                    gut_bact_list_path=gut_bact_list_path, verbose=True)