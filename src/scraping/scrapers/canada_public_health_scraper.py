# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
Public Health Agency of Canada crawler
Expected page to crawl is
https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19.html#faq
"""
__author__ = "Max Fleming", "Darius Irani"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Max Fleming", "Darius Irani"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import datetime
import time
import dateparser
import requests
from bs4 import BeautifulSoup
from covid_scraping import Conversion, Scraper


class CanadaPublicHealthScraper(Scraper):
    def _link_to_responce(self, link):
        """
        We only want to scrap Canada's public health.
        Many other links go to responses for financial aid an other public sites.
        """
        if link[0] is not '/':
            return None
        try:
            html = requests.get('https://www.canada.ca' + link)
            soup = BeautifulSoup(html.content, 'lxml').find(
                ['h2', 'h3'], {'id': link.split('#')[1]}).find_next_sibling()
            responce = str(soup)
            while soup.find_next_sibling() is not None and soup.find_next_sibling(
            ).name not in ['h2', 'h3', 'div']:
                soup = soup.find_next_sibling()
                responce += " " + str(soup)
            return responce
        except BaseException:
            return None

    def scrape(self):
        url = 'https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19.html#faq'
        html = requests.get(url).text
        soup = BeautifulSoup(
            html, 'lxml').find(
            'ul', {
                'class': 'list-unstyled'}).findAll('a')
        lastUpdatedTime = time.mktime(dateparser.parse(BeautifulSoup(html, 'lxml').find(
            'p', {'class': 'text-right h3 mrgn-tp-sm'}).getText()).timetuple())
        questions = [str(x) for x in soup]
        response_links = [x['href'] for x in soup]
        responses = list(map(self._link_to_responce, response_links))
        converter = Conversion(
            self._filename,
            self._path)
        for q, a in zip(questions, responses):
            if not a:  # no accompanying answer to question
                continue
            converter.addExample({
                'sourceUrl': url,
                'sourceName': "Public Health Agency of Canada",
                "needUpdate": True,
                "typeOfInfo": "QA",
                "isAnnotated": False,
                "responseAuthority": "",
                "question": q,
                "answer": a if a else "",
                "hasAnswer": a is not None,
                "targetEducationLevel": "NA",
                "topic": [],
                "extraData": {},
                "targetLocation": "Canada",
                "language": 'en',
            })
        return converter.write()


def main():
    scraper = CanadaPublicHealthScraper(
        path='./', filename='CanadaPublicHealth')
    scraper.scrape()


if __name__ == '__main__':
    main()
