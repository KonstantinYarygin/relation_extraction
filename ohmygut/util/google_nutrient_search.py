# -*- coding: utf-8 -*-
import time
import traceback
import urllib.request
import urllib.parse

import sys
from bs4 import BeautifulSoup
import random

from ohmygut.core import constants


def get_google_search_urls_html(html):
    parser = BeautifulSoup(html)
    result_blocks = parser('cite')
    if not result_blocks:
        return False
    list_of_urls = list(map(lambda x: x.text, result_blocks))
    return list_of_urls


def get_google_search_urls(query, results_number=100):
    """

    :param query: a string to search
    :param results_number:  a number of results, have to be
    :return:
    """
    list_of_urls = []
    results_per_page = 100
    page_number = results_number / results_per_page
    for i in range(1, page_number):
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            stream = opener.open(
                'https://www.google.ru/search?q=' + urllib.parse.quote(query) + '&num=%i' % results_number)
            html = stream.read()
        except:
            error = traceback.format_exc(sys.exc_info())
            constants.logger.error(error)
            return list_of_urls
        urls = get_google_search_urls_html(html)
        if urls:
            list_of_urls += urls
        else:
            break

        time.sleep(90)
    list_of_urls = list(set(list_of_urls))
    return list_of_urls


if __name__ == '__main__':
    start = time.time()
    list_of_url = get_google_search_urls('osiris therapeutics', 5)
    print(list_of_url)
