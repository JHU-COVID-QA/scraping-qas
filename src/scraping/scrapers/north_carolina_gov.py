# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
NorthCarolinaGovScraper crawler
Expected page to crawl is
https://www.ncdhhs.gov/divisions/public-health/covid19/frequently-asked-questions-about-covid-19
"""
__author__ = "Udit Sharma"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Udit Sharma"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import dateparser
import time
import requests
import os
from bs4 import BeautifulSoup, NavigableString, CData, Tag
from covid_scraping import Conversion, Scraper


class NorthCarolinaGovScraper(Scraper):

    def _extract_question(self, soup):
        return str(soup.find('h2', {'class': 'visuallyhidden'}).text)

    def _extract_answer(self, soup):
        lines = soup.findAll('p')
        lines_texts = []
        for line in lines:
            lines_texts.append(str(line.text))
        result = ' '.join(lines_texts)
        return result

    def _extract_topic(self, soup):
        return str(soup.find('h2', {'class': 'section-title'}).text)

    def scrape(self):
        name = 'North Carolina Public Health Division'
        url = 'https://www.ncdhhs.gov/divisions/public-health/covid19/frequently-asked-questions-about-covid-19'
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'lxml')
        sections = soup.findAll('section', {'class': 'entity entity-paragraphs-item paragraphs-item-accordion band no-gutter clearfix'})

        
        lastUpdateTime = time.time()
        converter = Conversion(
            self._filename,
            self._path,
            self._dateScraped,
            lastUpdateTime)

        for section in sections:
            topic = self._extract_topic(section)
            qa_blocks = section.findAll('section', {'class': 'tab-main no-aside'})
            for block in qa_blocks:
                question = self._extract_question(block)
                answer = self._extract_answer(block)
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
                    "topic": [topic],
                    "extraData": {},
                    "targetLocation": "North Carolina",
                    "language": "en"
                })
        return converter.write()


def main():
    scraper = NorthCarolinaGovScraper(path='./', filename='NorthCarolina')
    scraper.scrape()


if __name__ == '__main__':
    main()
