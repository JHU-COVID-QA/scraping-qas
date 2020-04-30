# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
NYTimes crawler
Expected page to crawl is
https://www.nytimes.com/interactive/2020/world/coronavirus-tips-advice.html
"""
__author__ = "Kaushik Srinivasan, Max Fleming"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Kaushik Srinivasan", "Adam Poliak"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import time
from urllib.request import urlopen
from bs4 import BeautifulSoup, NavigableString, CData, Tag
from covid_scraping import Conversion, Scraper


class NewYorkTimesScraper(Scraper):
    def scrape(self):
        name = 'NYTimes'
        url = 'https://www.nytimes.com/interactive/2020/world/coronavirus-tips-advice.html'
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")

        questions, answers = [], []
        for panelgroup in soup.findAll("div", {"class": "g-question-wrap"}):
            q = str(panelgroup.find('h3'))
            a = str(panelgroup.find('div', {'class': "g-answer-wrap"}))
            questions.append(q)
            answers.append(a)

        lastUpdateTime = time.mktime(
            time.strptime(
                soup.find('time').getText(),
                "Updated %B %d, %Y"))

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
                "targetLocation": "",
                "language": 'en'
            })
        return converter.write()


def main():
    scraper = NewYorkTimesScraper(path='./', filename='NYT')
    scraper.scrape()


if __name__ == '__main__':
    main()
