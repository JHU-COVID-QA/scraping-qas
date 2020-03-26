import requests
import textract
import re
import time
import subprocess
import jsonlines
import uuid

from covid_scraping import test_jsonlines


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
    lastUpdatedTime = time.mktime(time.strptime(re.search('\d+:\d+ \w+ \w+ \w+, \w+, \w+ \d+, \d+', text).group().replace("Central Time", ""), '%I:%M %p , %A, %B %d, %Y'))
    questions = []
    responces = []
    indexes = [[m.start(0), m.end(0)] for m in re.finditer("Q:|A:", text)]
    for i in range(0, len(indexes) - 2, 2):
        questions.append(text[indexes[i][1]:indexes[i+1][0]])
        responces.append(text[indexes[i+1][1]:indexes[i+2][0]])
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
            "topic":"",
            "extraData": {},
        })
    with jsonlines.open('../../../data/scraping/schema_v0.1/AVMA_v0.1.jsonl', 'w') as writer:
                writer.write_all(faq)

    test_jsonlines('../../../data/scraping/schema_v0.1/AVMA_v0.1.jsonl')


def main():
  generate_schema(scrape())

if __name__ == '__main__':
  main()
