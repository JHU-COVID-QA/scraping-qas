import datetime, time
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



def crawl():
    name = 'Texas Human Resources'
    url = 'https://www.dshs.state.tx.us/coronavirus/faq.aspx'
    html = requests.get(url, verify=False).text
    soup = BeautifulSoup(html, "lxml")

    #faq is in the second div
    faq = soup.find("div",{"id": "ctl00_ContentPlaceHolder1_uxContent"}).findAll("div", recursive=False)[1]
    lastUpdateTime = time.mktime(time.strptime(soup.find("span", {"lastUpdatedDate"}).getText().strip(), "%B %d, %Y"))

    questions, answers = [], []
    a = ''
    for e in faq.findAll(recursive=False):
        if e.name == 'h2':
            q = e.getText()
            a = ''
        elif e.name == 'hr':
            questions.append(q)
            answers.append(a)
        else:
            a += e.getText().strip() +'\n'

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

    with jsonlines.open('../../../data/scraping/TexasHumanResources_v0.1.jsonl', 'w') as writer:
            writer.write_all(faq)

    test_jsonlines('../../../data/scraping/TexasHumanResources_v0.1.jsonl')
    
if __name__ == "__main__":
    crawl()
