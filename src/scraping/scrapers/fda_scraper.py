# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
FDA crawler
Expected page to crawl is
https://www.fda.gov/emergency-preparedness-and-response/mcm-issues/coronavirus-disease-2019-covid-19-frequently-asked-questions
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
from urllib.request import urlopen
from bs4 import BeautifulSoup
from covid_scraping import Conversion, Scraper


class FDAScraper(Scraper):
    def scrape(self):
        name = 'FDA'
        url = 'https://www.fda.gov/emergency-preparedness-and-response/mcm-issues/coronavirus-disease-2019-covid-19-frequently-asked-questions'
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")
        questions, answers = [], []

        for panelgroup in soup.findAll("div", {"class": "panel-group"}):
            for qa in panelgroup.findAll('div', {"class": "panel"}):
                q = str(
                    qa.find("div", {"class": "panel-heading"})).replace('Q:', '')
                a = str(
                    qa.find("div", {"class": "panel-body"})).replace('A:', '')
                questions.append(q)
                answers.append(a)

        lastUpdateTime = time.mktime(
            time.strptime(
                soup.find(
                    "p",
                    {"lcds-description-list__item-text"}).getText().strip(),
                "%m/%d/%Y"))

        converter = Conversion(
            self._filename,
            self._path)
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
                "targetLocation": 'US',
                'language': 'en'
            })
        return converter.write()


def main():
    scraper = FDAScraper(path='./', filename='FDA')
    scraper.scrape()


if __name__ == '__main__':
    main()
