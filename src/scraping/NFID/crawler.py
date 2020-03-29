# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
NFID crawler
Expected page to crawl is
https://www.nfid.org/infectious-diseases/frequently-asked-questions-about-novel-coronavirus-2019-ncov/
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
import pprint
import requests
from bs4 import BeautifulSoup, NavigableString, CData, Tag
import jsonlines
import re
import pandas as pd
import uuid
import jsonlines
import time

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


faq = []


def crawl_common():
    name = 'National Foundation for Infectious Diseases'
    url = 'https://www.nfid.org/infectious-diseases/frequently-asked-questions-about-novel-coronavirus-2019-ncov/'
    html = requests.get(url, verify=False).text
    # All faq is in the entry-content
    soup = BeautifulSoup(html, 'lxml').find('div', {'class': 'entry-content'})
    date = re.compile(r'Updated \w+ \d+, \d+')
    for p in soup.find_all('p'):
        if re.match(date, p.getText()):
            lastUpdatedTime = time.mktime(
                time.strptime(p.getText()[8:], "%B %d, %Y"))
            break

    begin = False
    questions = []
    responces = []
    a = ''
    for e in soup.findAll(recursive=False):
        if e.name == 'h3' and not begin:
            q = e.getText()
            a = ''
            begin = True
        elif e.name == 'h3' and begin:
            questions.append(q)
            responces.append(a)
            containsURLs = False
            q = e.getText()
            a = ''
        elif e.name == 'p':
            a += ' ' + e.getText().strip()
        elif e.name == 'ul':
            pre_edit = e.getText()
            a += ' ' + pre_edit.replace('\n', '; ').replace(';', '', 1)
    questions.append(q)
    responces.append(
        a.split("View current guidance on the 2019 novel coronavirus.")[0])
    for q, a in zip(questions, responces):
        faq.append({
            'sourceUrl': url,
            'sourceName': name,
            "dateScraped": time.time(),
            "sourceDate": None,
            "lastUpdateTime": lastUpdatedTime,
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


def crawl_at_risk():
    name = 'National Foundation for Infectious Diseases'
    url = 'https://www.nfid.org/infectious-diseases/common-questions-and-answers-about-covid-19-for-older-adults-and-people-with-chronic-health-conditions/'
    html = requests.get(url, verify=False).text
    # All faq is in the entry-content
    soup = BeautifulSoup(html, 'lxml').find('div', {'class': 'entry-content'})
    date = re.compile(r'Updated: \w+ \d+, \d+')
    for p in soup.find_all('p'):
        if re.match(date, p.getText()):
            lastUpdatedTime = time.mktime(
                time.strptime(p.getText()[9:], "%B %d, %Y"))
            break

    begin = False
    questions = []
    responces = []
    a = ''
    for e in soup.findAll(recursive=False):
        if e.name == 'h3' and not begin:
            q = e.getText()
            a = ''
            begin = True
        elif e.name == 'h3' and begin:
            questions.append(q)
            responces.append(a)
            containsURLs = False
            q = e.getText()
            a = ''
        elif e.name == 'p':
            a += ' ' + e.getText().strip()
        elif e.name == 'ul':
            pre_edit = e.getText()
            a += ' ' + pre_edit.replace('\n', '; ').replace(';', '', 1)
    questions.append(q)
    responces.append(a.split("Updated: ")[0])
    link = re.compile(r'\S\.\S')
    for q, a in zip(questions, responces):
        faq.append({
            'sourceUrl': url,
            'sourceName': name,
            "dateScraped": time.time(),
            "sourceDate": None,
            "lastUpdateTime": lastUpdatedTime,
            "needUpdate": True,
            "containsURLs": bool(re.search(link, a)),
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


crawl_common()
crawl_at_risk()
with jsonlines.open('../../../data/scraping/schema_v0.1/' + diff + 'NFID_v0.1' + extension + '.jsonl', 'w') as writer:
    writer.write_all(faq)

test_jsonlines('../../../data/scraping/schema_v0.1/' +
               diff + 'NFID_v0.1' + extension + '.jsonl')
