# -*- coding: utf-8 -*-
import os
import time
import traceback
import urllib.request
import urllib.parse

import sys
from bs4 import BeautifulSoup
import random

from ohmygut.core import constants
from ohmygut.core.catalog.nutrients_catalog import NutrientsCatalogNikogosov

script_dir = os.path.dirname(os.path.realpath(__file__))


def get_google_search_urls_html(html):
    parser = BeautifulSoup(html, 'lxml')
    result_blocks = parser('cite')
    if not result_blocks:
        return []
    list_of_urls = list(map(lambda x: x.text, result_blocks))
    return list_of_urls


def get_google_search_urls(query, results_number=100):
    """

    :param query: a string to search
    :param results_number:  a number of results, have to be
    :return:
    """
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        stream = opener.open(
            'https://www.google.ru/search?q=' + urllib.parse.quote(query) + '&num=%i' % results_number)
        html = stream.read()
    except:
        error = traceback.format_exc(sys.exc_info())
        constants.logger.error(error)
        return []

    urls = get_google_search_urls_html(html)
    return urls


if __name__ == '__main__':
    constants.logger.info("start google nutrients")
    nutrients_catalog = NutrientsCatalogNikogosov(
        path=os.path.join(script_dir, '../../data/nutrients/nikogosov_nutrients_normalized.tsv'))
    nutrients_catalog.initialize(verbose=True)
    nutrients = nutrients_catalog.get_simple_list()
    nutrients.sort()
    i = 1
    for nutrient in nutrients:
        list_of_url = get_google_search_urls(nutrient, 100)
        for url in list_of_url:
            constants.google_search_nutrient_logger.info("%i\t%s\t%s" % (i, nutrient, url))
        time.sleep(90)
        i += 1
    constants.logger.info("finish google nutrients")
