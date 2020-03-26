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



def crawl_helper(name, url):
    html = urlopen(url)
    soup = BeautifulSoup(html, "lxml")

    main = soup.find("main", {"class":"col-lg-9"}).find("div", {"class":"content"})
    rows = main.findAll("div", {"class":"row"})


    if len(rows) > 1:
        lastUpdateTime = time.mktime(time.strptime(rows[0].getText().strip(), "Revisions were made on %B %d, %Y, to reflect updated guidance."))
    else:
        lastUpdateTime = None

    q, a = '',[]
    questions, answers = [], []
    for elem in rows[-1].find("div").findAll(recursive=False):
        if elem.name == "p":
            if elem.findAll("span"):
                for span in elem.findAll("span"):
                    span.decompose()
            if elem.find("strong"):
                if q and a:
                    a = "\n".join(a)
                    questions.append(q.replace("Q: ",""))
                    answers.append(a.replace("A: ",""))
                    q,a = '', []

                q = elem.find("strong").get_text()
                elem.strong.decompose()
                text = elem.getText()
                if text:
                    a.append(text)
            else:
                a.append(elem.getText())
        elif elem.name in ["ul", "ol"]:
            a.append(elem.get_text())

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
    return faq

def crawl():
    faq = crawl_helper("CDC Lab Biosafety", "https://www.cdc.gov/coronavirus/2019-ncov/lab/biosafety-faqs.html") + \
            crawl_helper("CDC Lab Diagnotic Tools and Virus", "https://www.cdc.gov/coronavirus/2019-ncov/lab/tool-virus-requests.html")

    with jsonlines.open('../../../data/scraping/schema_v0.1/CDCLab_v0.1.jsonl', 'w') as writer:
        writer.write_all(faq)

    test_jsonlines('../../../data/scraping/schema_v0.1/CDCLab_v0.1.jsonl')
    
if __name__ == "__main__":
    crawl()
