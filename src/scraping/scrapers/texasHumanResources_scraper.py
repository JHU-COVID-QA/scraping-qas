# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
Texas Human Resources crawler
Expected page to crawl is
https://www.dshs.state.tx.us/coronavirus/faq.aspx
"""
__author__ = "Shuo Sun, Max Fleming"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Shuo Sun"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import time
import requests
from bs4 import BeautifulSoup
from covid_scraping import Conversion, Scraper


class TexasHumanResourceScraper(Scraper):
    def scrape(self):
        name = 'Texas Human Resources'
        url = 'https://www.dshs.state.tx.us/coronavirus/faq.aspx'
        html = requests.get(url, verify=False).text
        soup = BeautifulSoup(html, "lxml")

        # faq is in the second div
        faq = soup.find(
            "div", {
                "id": "ctl00_ContentPlaceHolder1_uxContent"}).findAll(
            "div", recursive=False)[1]
        lastUpdateTime = time.mktime(
            time.strptime(
                soup.find(
                    "span",
                    {"lastUpdatedDate"}).getText().strip(),
                "%B %d, %Y"))
        questions, answers = [], []
        a = ''
        begun = False
        for e in faq.findAll(recursive=False):
            if e.name == 'h3':
                if begun:
                    questions.append(q)
                    answers.append(a)
                q = str(e)
                a = ''
                begun = True
            elif e.name == 'p' or e.name == 'ul':
                a += str(e)
        questions.append(q)
        answers.append(a)

        converter = Conversion(
            self._filename,
            self._path,
            self._dateScraped,
            lastUpdateTime)
        for question, answer in zip(questions, answers):
            converter.addExample({
                'sourceUrl': url,
                'sourceName': name,
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
                "targetLocation": "Texas",
                "language": 'en'
            })
        return converter.write()


def main():
    scraper = TexasHumanResourceScraper(path='./', filename='TexasHR')
    scraper.scrape()


if __name__ == '__main__':
    main()
