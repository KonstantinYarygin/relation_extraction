# -*- coding: utf-8 -*-
import os
import sys
import time
import traceback
import urllib.parse
import urllib.request

import pandas as pd
from bs4 import BeautifulSoup

from ohmygut.core.constants import google_search_logger

sys.path.append('.')

from ohmygut.core import constants
from ohmygut.util.sendmail import send_mail

script_dir = os.path.dirname(os.path.realpath(__file__))
output_file_name = 'nutrients_google.txt'


def get_google_search_urls_html(html):
    parser = BeautifulSoup(html, 'lxml')
    result_blocks = parser('cite')
    if not result_blocks:
        return []
    list_of_urls = list(map(lambda x: x.text, result_blocks))
    return list_of_urls


def get_google_search_urls(query, page_number):
    """

    :param page_number:
    :param query: a string to search
    :return:
    """
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    all_urls = set()
    results_per_page_number = 100
    for i in range(0, page_number):
        google_query = 'https://www.google.ru/search?q=%s&num=%i&start=%i' % (urllib.parse.quote(query),
                                                                              results_per_page_number,
                                                                              i * results_per_page_number)
        stream = opener.open(google_query)
        html = stream.read()
        urls = set(get_google_search_urls_html(html))
        constants.logger.info(urls)
        len_before = len(all_urls)
        all_urls = all_urls.union(urls)
        len_after = len(all_urls)
        if len_before == len_after:
            constants.logger.info("got repeated urls")
            time.sleep(90)
            break
        time.sleep(90)

    return all_urls


def do_search(strings_to_search):
    print("start google search")
    i = 1
    messages = []
    for string in strings_to_search:
        try:
            list_of_url = get_google_search_urls(string, page_number=10)
        except:
            error = traceback.format_exc()
            print(error)
            message = "%i\t%s\t%s" % (i, string, "ERROR")
            google_search_logger.info(message)
            messages.append(message)
            continue
        for url in list_of_url:
            message = "%i\t%s\t%s" % (i, string, url)
            google_search_logger.info(message)
            messages.append(message)
    print("finish google search")

    with open(output_file_name, 'w') as f:
        f.write('\n'.join(messages))

    send_mail("anatoly.developer@gmail.com",
              "[text-mining] google search",
              body="piping hot, sir",
              files=[output_file_name])


if __name__ == '__main__':
    data = pd.read_csv('food.csv', sep='\t')
    queries = list(data['foodgroup']) + list(data['food'])
    do_search(queries)
