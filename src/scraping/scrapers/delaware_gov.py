# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
Delaware State Government crawler
Expected page to crawl is
https://coronavirus.delaware.gov/what-delawareans-can-do/#faqs
"""
__author__ = "Nicola Ivanov"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Nicola Ivanov"]
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


class DelawareGovScraper(Scraper):
    def scrape(self):
        name = 'Delaware State Government'
        url = 'https://coronavirus.delaware.gov/what-delawareans-can-do/#faqs'
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")

        questions = [str(q)
                     for q in soup.findAll("h4", {"class": "panel-title"})]
        answers = [str(a)
                   for a in soup.findAll("div", {"class": "panel-body"})]

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
                "targetLocation": "Delaware",
                "language": "en"
            })
        return converter.write()


def main():
    scraper = DelawareGovScraper(path='./', filename='Delaware')
    scraper.scrape()


if __name__ == '__main__':
    main()
