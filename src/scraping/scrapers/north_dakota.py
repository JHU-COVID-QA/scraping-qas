# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
North Dakota crawler
Expected page to crawl is
https://ndresponse.gov/covid-19-resources/covid-19-faqs
"""
__author__ = "Max Fleming"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Max Fleming"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import time
import requests
from bs4 import BeautifulSoup, NavigableString, CData, Tag
from covid_scraping import Conversion, Scraper
import itertools


class NorthDakotaGovScraper(Scraper):

    def _extract_question(self, x):
        return str(x.find('a'))

    def _extract_answer(self, x):
        return " ".join([str(y) for y in x.findAll(['p', 'ol', 'ul'])])

    def scrape(self):
        name = 'North Dakota Stake Government'
        url = 'https://ndresponse.gov/covid-19-resources/covid-19-faqs'
        html = requests.get(url).text

        soup = BeautifulSoup(html, "lxml").findAll(
            'div', {'class': 'view-content'})[4].findAll('div', {'class': 'views-row'})
        soup = [x.findAll('div', {'class': 'views-row'}) for x in soup]
        soup = list(itertools.chain.from_iterable(soup))

        questions = list(map(self._extract_question, soup))
        answers = list(map(self._extract_answer, soup))
        converter = Conversion(
            self._filename,
            self._path,
            self._dateScraped,
            # No time stamp avalible on this page.
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
                "targetLocation": "North Dakota",
                "language": "en"
            })
        return converter.write()


def main():
    scraper = NorthDakotaGovScraper(path='./', filename='North_Dakota')
    scraper.scrape()


if __name__ == '__main__':
    main()
