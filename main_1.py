from article_data_loader import ArticleCatalog
from bacteria_catalog import BacteriaCatalog
from nutrient_catalog import NutrientCatalog
from sentence_processing import SentenceProcessor

article_catalog = ArticleCatalog('../article_data/texts/')
bacteria_catalog = BacteriaCatalog(verbose=False)
nutrient_catalog = NutrientCatalog(verbose=False)

for article in article_catalog[:10]:
    for sentence in article.full_text:
        bc_out = bacteria_catalog.find_bacteria(sentence)
        nc_out = nutrient_catalog.find_nutrient(sentence)
        if bc_out and nc_out:
            sentence_processor = SentenceProcessor(sentence)
            print(sentence_processor)
