# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
JHU HUB crawler
Expected page to crawl is
https://hub.jhu.edu/2020/03/23/how-to-self-quarantine-self-isolate/?mc_cid=0ed1a231a3&mc_eid=9687fd9d33
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
import requests
from bs4 import BeautifulSoup
from covid_scraping import Conversion, Scraper


class JHUHubScraper(Scraper):
    def _scrape(self, url, converter):
        html = requests.get(url).text
        lastUpdateTime = BeautifulSoup(html, 'lxml').find(
            'span', {'class': 'publish-date convert-pubdate'})['data-timestamp']
        soup = BeautifulSoup(
            html, 'lxml').findAll('h3')
        questions = [str(x) for x in soup]
        responces = [str(x.find_next()) for x in soup]
        for q, a in zip(questions, responces):
            converter.addExample({
                'sourceUrl': url,
                'sourceName': "JHU HUB",
                "sourceDate": 1584946800,
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
                "topic": ['self-quarantine', 'self-isolate'],
                "extraData": {},
                'targetLocation': '',
                'language': 'en'
            })

    def scrape(self):
        hub_links_to_scrape = ['https://hub.jhu.edu/2020/03/30/andrew-pekosz-immunity-seasonality/?fbclid=IwAR2LUcjr7Ltz6koe0IjRV3gr7E3tW0K6hqlcaYPtKQz3HBmjlQ7YRGrtgHw',
                               'https://hub.jhu.edu/2020/03/23/how-to-self-quarantine-self-isolate/?mc_cid=0ed1a231a3&mc_eid=9687fd9d33']
        converter = Conversion(self._filename, self._path)
        for link in hub_links_to_scrape:
            self._scrape(link, converter)
        return converter.write()


def main():
    scraper = JHUHubScraper(path="./", filename="JHU_Hub")
    scraper.scrape()

if __name__ == '__main__':
    main()
