# right (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
Hawaii State Government crawler
Expected page to crawl is
https://health.hawaii.gov/coronavirusdisease2019/what-you-should-know/faqs/
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
import dateparser
from bs4 import BeautifulSoup, NavigableString, CData, Tag
from covid_scraping import Conversion, Scraper


class HawaiiGovScraper(Scraper):
    def scrape(self):
        name = 'Hawaii State Government'
        url = 'https://health.hawaii.gov/coronavirusdisease2019/what-you-should-know/faqs/'
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")

        questions = [str(q)
                     for q in soup.findAll("h3")]

        answers = []
        for q in soup.findAll("h3"):
            a = ""
            for tag in q.next_siblings:
                if tag.name == "div":
                    break
                else:
                    a += str(tag)
            answers.append(a)

        lastUpdate = time.mktime(dateparser.parse(' '.join(soup.find(
                         'em').getText().split()[1:]), date_formats=['%B %d, %Y, %I %p']).timetuple())

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
                "targetLocation": "Hawaii",
                "language": "en"
            })
        return converter.write()


def main():
    scraper = HawaiiGovScraper(path='./', filename='Hawaii')
    scraper.scrape()


if __name__ == '__main__':
    main()
