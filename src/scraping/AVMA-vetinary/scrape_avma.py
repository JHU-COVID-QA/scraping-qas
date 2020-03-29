# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
AVMA crawler (pet related info)
Expected page to crawl is
https://www.avma.org/sites/default/files/2020-03/covid-19-faq-pet-owners.pdf
"""
__author__ = "Max Fleming"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Max Fleming", "Adam Poliak"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import requests
import textract
import re
import time
import subprocess
import jsonlines
import uuid

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


def scrape():
    text = ''
    url = 'https://www.avma.org/sites/default/files/2020-03/covid-19-faq-pet-owners.pdf'
    r = requests.get(url)
    with open('tmp.pdf', 'wb') as f:
        f.write(r.content)
    text = textract.process('tmp.pdf').decode()
    subprocess.call(['rm', 'tmp.pdf'])
    return text


def generate_schema(text):
    lastUpdatedTime = time.mktime(
        time.strptime(
            re.search(
                r'\d+:\d+ \w+ \w+ \w+, \w+, \w+ \d+, \d+',
                text).group().replace(
                "Central Time",
                ""),
            '%I:%M %p , %A, %B %d, %Y'))
    questions = []
    responces = []
    indexes = [[m.start(0), m.end(0)] for m in re.finditer("Q:|A:", text)]
    for i in range(0, len(indexes) - 2, 2):
        questions.append(text[indexes[i][1]:indexes[i + 1][0]])
        responces.append(text[indexes[i + 1][1]:indexes[i + 2][0]])
    faq = []
    for q, a in zip(questions, responces):
        faq.append({
            'sourceUrl': 'https://www.avma.org/sites/default/files/2020-03/covid-19-faq-pet-owners.pdf',
            'sourceName': 'AVMA',
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
    with jsonlines.open('../../../data/scraping/schema_v0.1/' + diff + 'AVMA_v0.1' + extension + '.jsonl', 'w') as writer:
        writer.write_all(faq)

    test_jsonlines('../../../data/scraping/schema_v0.1/' +
                   diff + 'AVMA_v0.1' + extension + '.jsonl')


def main():
    generate_schema(scrape())


if __name__ == '__main__':
    main()
