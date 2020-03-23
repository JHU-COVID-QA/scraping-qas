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
    name = 'FDA'
    url = 'https://www.fda.gov/emergency-preparedness-and-response/mcm-issues/coronavirus-disease-2019-covid-19-frequently-asked-questions'
    html = urlopen(url)
    soup = BeautifulSoup(html, "lxml")

    questions, answers = [], []
    for panelgroup in soup.findAll("div", {"class": "panel-group"}):
        for qa in panelgroup.findAll('div', {"class": "panel"}):
            q = qa.find("div", {"class": "panel-heading"}).getText().replace('Q:','').strip()
            a = qa.find("div", {"class": "panel-body"}).getText().replace('A:','').strip()
            questions.append(q)
            answers.append(a)

    lastUpdateTime = time.mktime(time.strptime(soup.find("p", {"lcds-description-list__item-text"}).getText().strip(), "%m/%d/%Y"))

    faq = []
    for question, answer in zip(questions, answers):
        faq.append({
            'sourceUrl': url,
            'sourceName': name,
            "dateScraped": time.time(),
            "sourceDate": None,
            "lastUpdateTime": lastUpdateTime,
            "needUpdate": True,
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

    with jsonlines.open('../../../data/scraping/FDA_v0.1.jsonl', 'w') as writer:
            writer.write_all(faq)

    test_jsonlines('../../../data/scraping/FDA_v0.1.jsonl')
    
if __name__ == "__main__":
    crawl()
