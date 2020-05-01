# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
Florida Gov crawler
Expected page to crawl is
https://floridahealthcovid19.gov/frequently-asked-questions/
"""
__author__ = "Max Fleming"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Max Fleming"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import dateparser
import time
import requests
from bs4 import BeautifulSoup, NavigableString, CData, Tag
from covid_scraping import Conversion, Scraper


class VermontGovScraper(Scraper):

    def _extract_question(self, x):
        return str(x.find('h4'))

    def _extract_answer(self, x):
        return str(x.find('div', {'class' : 'answer'}))

    def scrape(self):
        name = 'Kansas Department of Health'
        url = 'https://apps.health.vermont.gov/COVID/faq/'
        html = requests.get(url).text

        lastUpdateTime = time.mktime(dateparser.parse(BeautifulSoup(html, "lxml").find('p', {'class' : 'subtitle'})\
                        .getText().split('Updated:')[1].strip()).timetuple())

        soup = BeautifulSoup(html, "lxml").find('ul', {'class' : 'topics'}).findAll('li', {'class' : 'faq'})

        questions = list(map(self._extract_question, soup))
        answers = list(map(self._extract_answer, soup))

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
                "targetLocation": "Florida",
                "language": "en"
            })
        return converter.write()


def main():
    scraper = VermontGovScraper(path='./', filename='Vermont')
    scraper.scrape()


if __name__ == '__main__':
    main()
