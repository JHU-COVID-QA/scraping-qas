# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
AVMA crawler (pet related info)
Expected page to crawl is
https://www.avma.org/sites/default/files/2020-03/covid-19-faq-pet-owners.pdf
"""
__author__ = "Max Fleming"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Max Fleming", "Adam Poliak"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import requests
import time
from bs4 import BeautifulSoup
from covid_scraping import Scraper, Conversion

class AVMAScraper(Scraper):

    def scrape(self):
        url = 'https://www.avma.org/resources-tools/animal-health-and-welfare/covid-19/covid-19-faqs-pet-owners'
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'lxml')
        faq = soup.find('h3', {'id' : '1'})
        questions = []
        answers = []
        begun = False
        for e in faq.next_siblings:
            if e.name == 'h5':
                if begun:
                    questions.append(q)
                    answers.append(a)
                q = str(e)
                a = ''
                begun = True
            elif e.name == 'p':
                a += str(e)
        questions.append(q)
        answers.append(a)
        converter = Conversion(self._filename, self._path, self._dateScraped, time.time())
        for q, a in zip(questions, answers):
            converter.addExample({
                'sourceUrl': 'https://www.avma.org/sites/default/files/2020-03/covid-19-faq-pet-owners.pdf',
                'sourceName': 'AVMA',
                #No dates exist on the page
                "needUpdate": True,
                "containsURLs": False,
                "typeOfInfo": "QA",
                "isAnnotated": False,
                "responseAuthority": "",
                "question": q,
                "answer": a,
                "hasAnswer": True,
                "targetEducationLevel": "NA",
                "topic": ['pets', 'animals'],
                "extraData": {},
                "targetLocation": "US",
                'language' : 'en'
            })
        converter.write()


def main():
    scraper = AVMAScraper(path='./', filename='AVMA')
    scraper.scrape()


if __name__ == '__main__':
    main()
