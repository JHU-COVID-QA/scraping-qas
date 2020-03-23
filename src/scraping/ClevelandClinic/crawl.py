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

    name = 'Cleveland Clinic'
    url = 'https://newsroom.clevelandclinic.org/2020/03/18/frequently-asked-questions-about-coronavirus-disease-2019-covid-19/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, verify=False, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    faq= soup.find("div",{"class": "entry-content"})
    answers, questions = [], []

    q = ''
    a = ''
    for e in faq.findAll(recursive=False):
        if e.name == 'h5':
            if q and a:
                questions.append(q.replace('Q:','').strip())
                answers.append(a.replace('A:','').strip())

            q = e.getText()
            a = ''
        else:
            a += e.getText().strip() +'\n'
    if q and a:
        questions.append(q.replace('Q:','').strip())
        answers.append(a.replace('A:','').strip())


    lastUpdateTime = time.mktime(time.strptime(soup.find("h3", {"entry-sub-title"}).getText().strip(), "Updated %B %d, %Y at %I:%M %p."))

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

    with jsonlines.open('../../../data/scraping/ClevelandClinic_v0.1.jsonl', 'w') as writer:
            writer.write_all(faq)

    test_jsonlines('../../../data/scraping/ClevelandClinic_v0.1.jsonl')
    
if __name__ == "__main__":
    crawl()
