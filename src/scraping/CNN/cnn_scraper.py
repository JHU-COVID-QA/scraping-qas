# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
CNN crawler
Expected page to crawl is
https://www.cnn.com/interactive/2020/health/coronavirus-questions-answers/
"""
__author__ = "Darius Irani"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Darius Irani"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import time
import requests
import dateparser
from bs4 import BeautifulSoup
from collections import namedtuple
from covid_scraping import Conversion, Scraper


class CNNScraper(Scraper):

    def scrape(self):
        Block = namedtuple('Block', 'content tags')
        extra_data = {}

        url = 'https://www.cnn.com/interactive/2020/health/coronavirus-questions-answers/'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        lastUpdatedTime = time.mktime(dateparser.parse(' '.join(soup.find(
            'div', {'class': 'cnnix-timestamp'}).getText().split()[1:]), date_formats=['%B %d, %Y, %I %p']).timetuple())

        tags = [tag.get('data-topic')
                for tag in soup.find_all('div', attrs={'class': 'nav-button'})]

        body = soup.find_all('div', attrs={'class': 'interactive-container'})[1]

        blocks = []
        for div in body.find_all('div'):
            if 'question' == div.get('class')[0]:
                tags = div.get('class')[1:]
                block = Block(div, tags)
                blocks.append(block)

        questions, answers, topics = [], [], []
        for block in blocks:
            question = block.content.find('div', attrs={'class': 'question-q'})
            answer = block.content.find('div', attrs={'class': 'question-a'})
            questions.append(str(question))
            answers.append(str(answer))
            topics.append(block.tags)

        converter = Conversion(self._filename, self._path)
        for q, a, t in zip(questions, answers, topics):
            converter.addExample({
                    'sourceUrl': url,
                    'sourceName': "CNN",
                    "sourceDate": lastUpdatedTime,
                    "lastUpdateTime": lastUpdatedTime,
                    "needUpdate": True,
                    "typeOfInfo": "QA",
                    "isAnnotated": False,
                    "responseAuthority": "",
                    "question": q,
                    "answer": a,
                    "hasAnswer": a is not None,
                    "targetEducationLevel": "NA",
                    "topic": t,
                    "extraData": {},
                    "targetLocation": "United States",
                    "language": 'en',
                })
        return converter.write()


def main():
    scraper = CNNScraper(path='.', filename='CNN')
    scraper.scrape()

if __name__ == '__main__':
    main()
