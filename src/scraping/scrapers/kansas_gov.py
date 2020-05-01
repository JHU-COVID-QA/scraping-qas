# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
Kansas Gov crawler
Expected page to crawl is
https://ks-kdhecovid19.civicplus.com/faq.aspx
"""
__author__ = "Max Fleming"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Max Fleming"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import datetime
import time
import requests
from bs4 import BeautifulSoup, NavigableString, CData, Tag
from covid_scraping import Conversion, Scraper


class KansasGovScraper(Scraper):

    def _extract_question(self, x):
        return str(x.find('a'))

    def _extract_answer(self, x):
        return " ".join([str(y) for y in x.findAll(['p', 'ul'])])

    def scrape(self):
        name = 'Kansas Department of Health and Enviroment'
        url = 'https://ks-kdhecovid19.civicplus.com/faq.aspx'
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml").find('div', {'id' : 'modulecontent'}).findAll('dl')

        questions = list(map(self._extract_question, soup))
        answers = list(map(self._extract_answer, soup))

        converter = Conversion(
            self._filename,
            self._path,
            self._dateScraped,
            time.time())
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
                "targetLocation": "Kansas",
                "language": "en"
            })
        return converter.write()


def main():
    scraper = KansasGovScraper(path='./', filename='Kansas')
    scraper.scrape()


if __name__ == '__main__':
    main()
