# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
Florida Gov crawler
Expected page to crawl is
https://floridahealthcovid19.gov/frequently-asked-questions/
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
from urllib.request import urlopen
from bs4 import BeautifulSoup, NavigableString, CData, Tag
from covid_scraping import Conversion, Scraper


class FloridaGovScraper(Scraper):
    def scrape(self):
        name = 'FloridaGov'
        url = 'https://floridahealthcovid19.gov/frequently-asked-questions/'
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")

        questions = [str(q)
                     for q in soup.findAll("h4", {"class": "panel-title"})]
        answers = [str(a)
                   for a in soup.findAll("div", {"class": "panel-body"})]

        lastUpdateTime = time.mktime(
            dateparser.parse(
                soup.find(
                    "div", {
                        "class": "header-bottom__timestamp"}).getText().strip().replace(
                    "Updated ", "")).timetuple())

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
                "targetLocation": "Florida",
                "language": "en"
            })
        return converter.write()


def main():
    scraper = FloridaScraper(path='./', filename='Florida')
    scraper.scrape()


if __name__ == '__main__':
    main()
