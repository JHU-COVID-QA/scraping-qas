# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
NFID crawler
Expected page to crawl is
https://www.nfid.org/infectious-diseases/frequently-asked-questions-about-novel-coronavirus-2019-ncov/
"""
__author__ = "Max Fleming, Adam Poliak"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Max Felming"]
__license__ = "Apache 2.0, Adam Poliak"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import time
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

from covid_scraping import Conversion, Scraper


class NFIDScraper(Scraper):

    def _crawl_common(self):
        faq = []
        name = 'National Foundation for Infectious Diseases'
        url = 'https://www.nfid.org/infectious-diseases/frequently-asked-questions-about-novel-coronavirus-2019-ncov/'
        html = requests.get(url).text
        # All faq is in the entry-content
        soup = BeautifulSoup(html, 'lxml').find(
            'div', {'class': 'entry-content'})
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
                "needUpdate": True,
                "typeOfInfo": "QA",
                "isAnnotated": False,
                "responseAuthority": "",
                "question": q,
                "answer": a,
                "hasAnswer": True,
                "targetEducationLevel": "NA",
                "targetLocation": "",
                "topic": [""],
                "extraData": {},
                'language': 'en'
            })
        return faq, lastUpdatedTime

    def _crawl_at_risk(self):
        faq = []
        name = 'National Foundation for Infectious Diseases'
        url = 'https://www.nfid.org/infectious-diseases/common-questions-and-answers-about-covid-19-for-older-adults-and-people-with-chronic-health-conditions/'
        html = requests.get(url).text
        # All faq is in the entry-content
        soup = BeautifulSoup(html, 'lxml').find(
            'div', {'class': 'entry-content'})
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
                "needUpdate": True,
                "typeOfInfo": "QA",
                "isAnnotated": False,
                "responseAuthority": "",
                "question": q,
                "answer": a,
                "hasAnswer": True,
                "targetEducationLevel": "NA",
                "targetLocation": "",
                "topic": [""],
                "extraData": {},
                "language": "en"
            })
        return faq, lastUpdatedTime

    def scrape(self):
        success = True
        examples, lastUpdateTime = self._crawl_common()
        converter = Conversion(
            self._filename,
            self._path,
            self._dateScraped,
            lastUpdateTime)
        for example in examples:
            converter.addExample(example)
        success &= converter.write()

        examples, lastUpdateTime = self._crawl_at_risk()
        converter = Conversion(
            self._filename,
            self._path,
            self._dateScraped,
            lastUpdateTime)
        for example in examples:
            converter.addExample(example)
        success &= converter.write()
        return success


def main():
    scraper = NFIDScraper(path="./", filename="NFID")
    scraper.scrape()


if __name__ == '__main__':
    main()
