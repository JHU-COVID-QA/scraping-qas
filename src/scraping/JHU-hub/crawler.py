# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
JHU HUB crawler
Expected page to crawl is
https://hub.jhu.edu/2020/03/23/how-to-self-quarantine-self-isolate/?mc_cid=0ed1a231a3&mc_eid=9687fd9d33
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


def crawl():
    url = 'https://hub.jhu.edu/2020/03/23/how-to-self-quarantine-self-isolate/?mc_cid=0ed1a231a3&mc_eid=9687fd9d33'
    html = requests.get(url, verify=False).text
    lastUpdateTime = BeautifulSoup(html, 'lxml').find(
        'span', {'class': 'publish-date convert-pubdate'})['data-timestamp']
    soup = BeautifulSoup(
        html, 'lxml').findAll('h3')
    questions = [x.getText().strip() for x in soup]
    responces = [x.find_next().getText().strip() for x in soup]
    faq = []
    for q, a in zip(questions, responces):
        faq.append({
            'sourceUrl': url,
            'sourceName': "JHU HUB",
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
            "targetEducationLevel": "NA",
            "topic": "",
            "extraData": {},
        })
    with jsonlines.open('../../../data/scraping/schema_v0.1/' + diff + 'JHU-hub_v0.1' + extension + '.jsonl', 'w') as writer:
        writer.write_all(faq)

    test_jsonlines(
        '../../../data/scraping/schema_v0.1/' +
        diff +
        'JHU-hub_v0.1' +
        extension +
        '.jsonl')


def main():
    crawl()


if __name__ == '__main__':
    main()
