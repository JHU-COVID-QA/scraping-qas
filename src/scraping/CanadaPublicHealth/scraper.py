# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
Public Health Agency of Canada crawler
Expected page to crawl is
https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19.html#faq
"""
__author__ = "Max Fleming"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Max Felming"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import datetime
import time
import dateparser
import json
import subprocess
import uuid
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup, NavigableString, CData, Tag
import re
import jsonlines
import copy

from covid_scraping import Conversion
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--rescrape", action='store_true')
args = parser.parse_args()
diff = ''
extension = ''
if args.rescrape:
    diff = 'stage/'
    extension = '_STAGE'


def link_to_responce(link):
    """
    We only want to scrap Canada's public health.
    Many other links go to responces for financial aid an other public sites.
    """
    if link[0] is not '/':
        return None
    try:
        html = requests.get('https://www.canada.ca' + link, verify=False)
        soup = BeautifulSoup(html.content, 'lxml').find(
            ['h2', 'h3'], {'id': link.split('#')[1]}).find_next_sibling()
        responce = str(soup)
        while soup.find_next_sibling() is not None and soup.find_next_sibling().name not in ['h2', 'h3', 'div']:
            soup = soup.find_next_sibling()
            responce += " " + str(soup)
        return responce
    except BaseException:
        print('Unable to scrape ' + 'https://www.canada.ca' + link)
        return None


def crawl():
    url = 'https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19.html#faq'
    html = requests.get(url, verify=False).text
    soup = BeautifulSoup(
        html, 'lxml').find(
        'ul', {
            'class': 'list-unstyled'}).findAll('a')
    lastUpdatedTime = time.mktime(dateparser.parse(BeautifulSoup(html, 'lxml').find(
        'p', {'class': 'text-right h3 mrgn-tp-sm'}).getText()[:-4], '%B %d, %Y, %I %p').timetuple())
    questions = [str(x) for x in soup]
    response_links = [x['href'] for x in soup]
    responces = list(map(link_to_responce, response_links))
    converter = Conversion('CanadaPublicHealth', '../../../data/scraping')
    for q, a in zip(questions, responces):
        converter.addExample({
                'sourceUrl': url,
                'sourceName': "Public Health Agency of Canada",
                "sourceDate": None,
                "lastUpdateTime": lastUpdatedTime,
                "needUpdate": True,
                "typeOfInfo": "QA",
                "isAnnotated": False,
                "responseAuthority": "",
                "question": q,
                "answer": a if a else "",
                "hasAnswer": a is not None,
                "targetEducationLevel": "NA",
                "topic": [],
                "extraData": {},
                "targetLocation": "Canada",
                "language": 'en',
            })
    converter.write()


def main():
    crawl()


if __name__ == '__main__':
    main()
