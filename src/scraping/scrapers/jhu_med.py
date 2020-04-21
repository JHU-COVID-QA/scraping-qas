# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
JHU Medicine crawler
Expected page to crawl is
https://www.hopkinsmedicine.org/health/conditions-and-diseases/coronavirus/coronavirus-frequently-asked-questions
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
import dateparser
import requests
import copy
from bs4 import BeautifulSoup
from covid_scraping import Conversion, Scraper


class JHUMedicineScraper(Scraper):

    def scrape(self):
        url = "https://www.hopkinsmedicine.org/health/conditions-and-diseases/coronavirus/coronavirus-frequently-asked-questions"
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'lxml').find_all('div', {'class': 'rtf'})
        lastUpdateTime = time.mktime(
                            dateparser.parse(
                            soup[-1].getText().strip()[7:])
                            .timetuple())

        final_questions = []
        final_responces = []
        for section in soup:
            questions = section.find_all('h3')
            for question in questions:
                final_questions.append(question.get_text(strip=False))
                soup_iter = question
                answer = ""
                while soup_iter.find_next_sibling() and soup_iter.find_next_sibling().name in ['p', 'ul']:
                    soup_iter = soup_iter.find_next_sibling()
                    answer += " " + str(soup_iter)
                final_responces.append(answer)
        converter = Conversion(self._filename, self._path)
        for q, a in zip(final_questions, final_responces):
            converter.addExample({
                'sourceUrl': url,
                'sourceName': "JHU Medicine",
                "sourceDate": lastUpdateTime,
                "lastUpdateTime": lastUpdateTime,
                "needUpdate": True,
                "containsURLs": False,
                "typeOfInfo": "QA",
                "isAnnotated": False,
                "responseAuthority": "",
                "question": q,
                "answer": a,
                "hasAnswer": True,
                "targetEducationLevel": "NA",
                "topic": [],
                "extraData": {},
                'targetLocation': '',
                'language': 'en'
            })
        return converter.write()


def main():
    scraper = JHUMedicineScraper(path=".", filename="JHU_Medicine")
    scraper.scrape()

if __name__ == '__main__':
    main()
