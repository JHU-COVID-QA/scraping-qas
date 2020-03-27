# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
NFID crawler
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

import datetime, time
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
parser.add_argument("--rescrape",action='store_true')
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
        soup = BeautifulSoup(html.content, 'lxml').find(['h2', 'h3'],{'id':link.split('#')[1]}).find_next()
        responce = soup.getText().strip()
        while soup.find_next().name not in ['h2', 'h3', 'div']:
            soup = soup.find_next()
            responce += " " + soup.getText().strip()
        return responce
    except:
        print('Unable to scrape ' + 'https://www.canada.ca' + link)
        return None

def crawl():
    url = 'https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19.html#faq'
    html = requests.get(url, verify=False).text
    soup = BeautifulSoup(html, 'lxml').find('ul',{'class':'list-unstyled'}).findAll('a')
    lastUpdatedTime = time.mktime(time.strptime(BeautifulSoup(html, 'lxml').find('p',{'class':'text-right h3 mrgn-tp-sm'}).getText()[:-4], '%B %d, %Y, %I %p'))
    questions = [x.getText().strip() for x in soup]
    response_links = [x['href'] for x in soup]
    responces = list(map(link_to_responce, response_links))
    faq = []
    for q, a in zip(questions, responces):
                faq.append({
                    'sourceUrl': url,
                    'sourceName': "Public Health Agency of Canada",
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
                    "answerText": a if a is not None else '' ,
                    "hasAnswer": a is not None,
                    "targetEducationLevel": "NA",
                    "topic":"",
                    "extraData": {},
                })
    with jsonlines.open('../../../data/scraping/schema_v0.1/' + diff + 'CanadaPublicHealth_v0.1' + extension + '.jsonl', 'w') as writer:
                writer.write_all(faq)

    test_jsonlines('../../../data/scraping/schema_v0.1/' + diff + 'CanadaPublicHealth_v0.1' + extension + '.jsonl')

def main():
    crawl()

if __name__ == '__main__':
  main()
