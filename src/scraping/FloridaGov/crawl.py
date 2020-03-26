# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
Florida Gov crawler
Expected page to crawl is 
https://floridahealthcovid19.gov/faq/
"""
__author__ = "Shuo Sun"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Shuo Sun"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import datetime, time
import pprint
from urllib import request, response, error, parse
from urllib.request import urlopen
from bs4 import BeautifulSoup, NavigableString, CData, Tag
import jsonlines
import re
import pandas as pd
import uuid
import jsonlines
import time

from covid_scraping import test_jsonlines



def crawl():
    name = 'FloridaGov'
    url = 'https://floridahealthcovid19.gov/faq/'
    html = urlopen(url)
    soup = BeautifulSoup(html, "lxml")

    questions = [q.getText().strip() for q in soup.findAll("h4", {"class": "panel-title"})]
    answers = [a.getText().strip() for a in soup.findAll("div", {"class": "panel-body"})]

    faq = []

    for question, answer in zip(questions, answers):
        faq.append({
            'sourceUrl': url,
            'sourceName': name,
            "dateScraped": time.time(),
            "sourceDate": None,
            "lastUpdateTime": None,
            "needUpdate": False,
            "containsURLs": "https://" in answer or "http://" in answer,
            "typeOfInfo": "QA",
            "isAnnotated": False,
            "responseAuthority": "",
            "questionUUID": str(uuid.uuid1()),
            "answerUUID": str(uuid.uuid1()),
            "exampleUUID": str(uuid.uuid1()),
            "questionText": question,
            "answerText": answer,
            "hasAnswer": True,
            "targetEducationLevel": "NA",
            "topic":"",
            "extraData": {},
        })

    with jsonlines.open('../../../data/scraping/FloridaGov_v0.1.jsonl', 'w') as writer:
            writer.write_all(faq)

    test_jsonlines('../../../data/scraping/FloridaGov_v0.1.jsonl')
    
if __name__ == "__main__":
    crawl()
