# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
Cleveland Clinic crawler
Expected page to crawl is
https://www.avma.org/sites/default/files/2020-03/covid-19-faq-pet-owners.pdf
"""
__author__ = "Shuo Sun, Max Fleming"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Shuo Sun"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import datetime
import time
import dateparser
import requests
from bs4 import BeautifulSoup, NavigableString, CData, Tag

from covid_scraping import Conversion, Scraper


class ClevelandScraper(Scraper):
    def scrape(self):
        name = 'Cleveland Clinic'
        url = 'https://newsroom.clevelandclinic.org/2020/03/18/frequently-asked-questions-about-coronavirus-disease-2019-covid-19/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(url, verify=False, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")

        faq = soup.find("div", {"class": "entry-content"})
        answers, questions = [], []

        q = ''
        a = ''
        for e in faq.findAll(recursive=False):
            if e.name == 'h5':
                if q and a:
                    questions.append(q.replace('Q:', ''))
                    answers.append(a.replace('A:', ''))

                q = str(e)
                a = ''
            else:
                a += " " + str(e)
        if q and a:
            questions.append(q.replace('Q:', ''))
            answers.append(a.replace('A:', ''))

        lastUpdateTime = time.mktime(
            dateparser.parse(
                soup.find(
                    "h3",
                    {"entry-sub-title"}).getText().strip().replace("Updated ", "")).timetuple())

        converter = Conversion(self._filename, self._path)
        for question, answer in zip(questions, answers):
            converter.addExample({
                'sourceUrl': url,
                'sourceName': name,
                "sourceDate": lastUpdateTime,
                "lastUpdateTime": lastUpdateTime,
                "needUpdate": True,
                "typeOfInfo": "QA",
                "isAnnotated": False,
                "responseAuthority": "",
                "question": question,
                "answer": answer,
                "hasAnswer": True,
                "targetEducationLevel": "NA",
                "topic": [],
                "extraData": {},
                "targetLocation": "Cleveland",
                "language": "en"
            })
        return converter.write()


def main():
    scraper = ClevelandScraper(path='./', filename='Cleveland')
    scraper.scrape()


if __name__ == '__main__':
    main()
