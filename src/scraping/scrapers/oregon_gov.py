# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
OregonGovScraper crawler
Expected page to crawl is
https://www.oregon.gov/oha/PH/DISEASESCONDITIONS/DISEASESAZ/Pages/COVID19-FAQ.aspx
"""
__author__ = "Udit Sharma"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Udit Sharma"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
import dateparser
import time
import requests
import os
from selenium import webdriver
from bs4 import BeautifulSoup, NavigableString, CData, Tag
from covid_scraping import Conversion, Scraper


class OregonGovScraper(Scraper):

    def _extract_question(self, soup):
        return str(soup.text)

    def _extract_answer(self, soup):
        return str(soup.text)

    def _extract_topic(self, soup):
        return str(soup.text)

    def scrape(self):
        chrome_driver_path = os.environ['CHROME_DRIVER_PATH']
        name = 'Oregon Public Health Division'
        url = 'https://www.oregon.gov/oha/PH/DISEASESCONDITIONS/DISEASESAZ/Pages/COVID19-FAQ.aspx?wp1284=l:100'
        opts = Options()
        opts.set_headless()
        driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=opts)
        driver.get(url)
        try:
            WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.TAG_NAME, 'td')))
        except:
            return False
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        questions = soup.findAll('td', {'data-title': 'Question'})
        answers = soup.findAll('td', {'data-title': 'Answer'})
        topics = soup.findAll('td', {'data-title': 'Topic'})

        lastUpdateTime = time.time()

        converter = Conversion(
            self._filename,
            self._path)

        for t, q, a in zip(topics, questions, answers):
            topic = self._extract_topic(t)
            question = self._extract_question(q)
            answer = self._extract_answer(a)

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
                "targetLocation": "Oregon",
                "language": "en"
            })

        driver.quit()
        return converter.write()


def main():
    scraper = OregonGovScraper(path='./', filename='Oregon')
    scraper.scrape()

if __name__ == '__main__':
    main()
