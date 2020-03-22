import argparse
import pandas as pd
import uuid
import jsonlines
import os
import time
import requests
import PyPDF2
import re
import itertools
from urllib.parse import urlparse
from urllib.request import urlretrieve
from collections import defaultdict, namedtuple
from bs4 import BeautifulSoup, NavigableString, Tag
from datetime import datetime as dt

KEYWORDS = ['covid-19', 'coronavirus']

def get_args():
    parser = argparse.ArgumentParser(description="Scrape resources from Medicaid.")
    parser.add_argument('resource_url', metavar='link to sites covid resources', type=str)
    args = parser.parse_args()
    return args


def to_schema(row):
    # ['Question', 'Answer', 'Need to update (Y/N)', 'Tags', 'Author']

    data = {
    "sourceUrl": "https://www.medicaid.gov/state-resource-center/disaster-response-toolkit/covid19/index.html",
    "sourceName": "Medicaid",
    "dateScraped": 1584717464,
    "sourceDate": 1584717464,
    "lastUpdateTime": 1584717464,
    "needUpdate": 1,
    "containsURLs": 0,
    "typeOfInfo": "QA",
    "isAnnotated": 1,
    "responseAuthority": "NA",
    "questionUUID": str(uuid.uuid1()),
    "answerUUID": str(uuid.uuid1()),
    "examplUUID": str(uuid.uuid1()),
    "questionText": row['Question'],
    "answerText": row['Answer'] if not pd.isna(row['Answer']) else "",
    "hasAnswer": not pd.isna(row['Answer']),
    "targetEducationLevel": "NA",
    "topic": row['Tags'] if not pd.isna(row['Tags']) else "",
    "extraData": {}}
    return data


def get_rsrc_links(page_url):
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = []
    for h in soup.find_all('h2'):
        header = h.text
        next_node = h.nextSibling
        while next_node is not None:
            if isinstance(next_node, Tag):
                if next_node.name == "h2":
                    break
                for link in next_node.find_all('a'):
                    url = link.get('href')
                    if url.startswith('/'):
                        url = 'https://www.medicaid.gov' + url
                    is_pdf = True if url.endswith('.pdf') else False
                    if urlparse(url).netloc in ['www.medicaid.gov', 'www.cms.gov']:
                        links.append((header, link.text, url, time.mktime(dt.now().timetuple()), is_pdf))
            next_node = next_node.nextSibling

    return pd.DataFrame(links, columns=['header', 'name', 'url', 'time_accessed', 'is_pdf'])


def extract_from_pdf(file):
    filename, headers = urlretrieve(row.url)
    with open(filename, 'rb') as obj:
        pdfReader = PyPDF2.PdfFileReader(obj)
        for page_num in range(pdfReader.numPages):
            page = pdfReader.getPage(page_num)
            text = page.extractText()
            import pdb; pdb.set_trace()


def extract_from_link(url):
    print("here", url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    import pdb; pdb.set_trace()
    # with open(file, 'rb') as obj:
    #     import pdb; pdb.set_trace()


def build_rsrc_df(links):
    df = pd.DataFrame(columns=['Type', 'Question', 'Answer', 'Topic', 'Extra'])
    for i, row in links.iterrows():
        if row.url.endswith('.pdf'):
            pass
            # df.append(extract_from_pdf(row.url))
        else:
            df.append(extract_from_link(row.url))
        

def main(args):
    links = get_rsrc_links(args.resource_url)
    build_rsrc_df(links)
    # links.to_csv('medicaid_resources.csv', index=False)
    # print(links)

    # df = pd.read_csv("COVID19infosheet - Info.tsv", sep="\t")
    # df['json'] = df.apply(to_schema, axis=1)

    # with jsonlines.open('../../../data/scraping/interalCOVIDinfosheet_v0.1.jsonl', 'w') as writer:
    #     writer.write_all(df['json'])


if __name__ == '__main__':
    args = get_args()
    main(args)