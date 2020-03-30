# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
JHU bloomberg crawler
Expected page to crawl is
https://www.globalhealthnow.org/2020-02/coronavirus-expert-reality-check
"""
__author__ = "Max Fleming"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Max Fleming"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import datetime
import time
import json
import subprocess
import uuid
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup, NavigableString, CData, Tag
import re
import jsonlines
from covid_scraping import test_jsonlines
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--rescrape", action='store_true')
args = parser.parse_args()
diff = ''
extension = ''
if args.rescrape:
    diff = 'stage/'
    extension = '_STAGE'


def filter_h3_headers(x):
    return not x.find('a')


def get_responces(x):
    x = x.find_next_sibling()
    responce = ''
    while x.find_next_sibling().find_next_sibling().name is 'p':
        responce += ' ' + x.getText().strip()
        x = x.find_next_sibling()
    return responce


def get_final_responce(x):
    x = x.find_next_sibling()
    responce = ''
    while 'dkerecm1' not in x.find_next_sibling().find_next_sibling().getText():
        responce += ' ' + x.getText().strip()
        x = x.find_next_sibling()
    return responce


def crawl():
    url = 'https://www.globalhealthnow.org/2020-02/coronavirus-expert-reality-check'
    html = requests.get(url, verify=False).text
    lastUpdateTime = time.mktime(time.strptime(BeautifulSoup(html, 'lxml').find('div', {'class': 'article-meta-wrap'}).getText().strip(), '%B %d, %Y'))
    soup = BeautifulSoup(
        html, 'lxml').find('div', {'property': 'schema:text'}).findAll('h3')
    questions_list = list(filter(filter_h3_headers, soup))
    questions = [x.getText().strip() for x in questions_list]
    responces = list(map(get_responces, questions_list[:-1]))
    responces.append(get_final_responce(questions_list[-1]))
    faq = []
    for q, a in zip(questions, responces):
        faq.append({
            'sourceUrl': url,
            'sourceName': "Johns Hopkins Bloomberg School of Public Health",
            "dateScraped": time.time(),
            "sourceDate": None,
            "lastUpdateTime": lastUpdateTime,
            "needUpdate": True,
            "containsURLs": False,
            "typeOfInfo": "QA",
            "isAnnotated": False,
            "responseAuthority": "",
            "questionUUID": str(uuid.uuid1()),
            "answerUUID": str(uuid.uuid1()),
            "exampleUUID": str(uuid.uuid1()),
            "questionText": q,
            "answerText": a,
            "hasAnswer": True,
            "targetEducationLevel": "College",
            "topic": "",
            "extraData": {},
        })
    with jsonlines.open('../../../data/scraping/schema_v0.1/' + diff + 'JHU-bloomberg_v0.1' + extension + '.jsonl', 'w') as writer:
        writer.write_all(faq)

    test_jsonlines(
        '../../../data/scraping/schema_v0.1/' +
        diff +
        'JHU-bloomberg_v0.1' +
        extension +
        '.jsonl')


def main():
    crawl()


if __name__ == '__main__':
    main()
