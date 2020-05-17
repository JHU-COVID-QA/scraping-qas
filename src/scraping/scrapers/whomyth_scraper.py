# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
WHO Myth crawler
Expected page to crawl is
https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters
"""
__author__ = "Kenton Murray, Max Fleming"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Kenton Murray"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import datetime
import time
import pprint
import uuid
from urllib import request, response, error, parse
from urllib.request import urlopen
from bs4 import BeautifulSoup, NavigableString, CData, Tag
import json
import jsonlines
from covid_scraping import Conversion, Scraper

'''
<div class="sf-content-block content-block" >
    <div ><h2></h2><h2><strong>COVID-19 virus can be transmitted in areas with hot and humid climates <o:p></o:p></strong></h2><p>From the
evidence so far, the COVID-19 virus can be transmitted in ALL AREAS, including areas with
hot and humid weather. Regardless of climate, adopt protective measures if you
live in, or travel to an area reporting COVID-19. The best way to
protect yourself against COVID-19 is by frequently cleaning your hands. By
doing this you eliminate viruses that may be on your hands and avoid infection
that could occur by then touching your eyes, mouth, and nose.<o:p></o:p></p><p>&nbsp;</p></div>

</div>

Unfortunately, the "sf-content-block" has a lot of other times it is used but are not questions. I naively look for <h2> which is a bolded question

Originally written by @KentonMurray so direct questions to him

'''


class WhoMythScraper(Scraper):
    def scrape(self):
        url = 'https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters'
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")
        qas_plus_some = soup.find_all(
            'div', class_='sf-content-block content-block')
        qa_pairs = []
        for potential in qas_plus_some:
            for child in potential.children:
                if "h2" in str(
                        child):  # Super hacky ... but this seemed to be the best way for this site
                    s_child = str(child)
                    s_child = s_child.replace("\n", " ")
                    s_child = s_child.replace(u'\xa0', u' ')
                    qa = s_child.split("</h2>")
                    if len(qa) == 2:
                        question = str(qa[0])
                        answer = str(qa[1])
                    elif len(qa) == 3:  # First question is different
                        question = str(qa[1])
                        answer = str(qa[2])
                    else:
                        print("ERROR:")  # TODO: better error handling?
                    qa_pairs.append((question, answer))
        converter = Conversion(
            self._filename,
            self._path)
        for pair in qa_pairs:
            converter.addExample({
                "sourceName": 'WHOMyth',
                "sourceUrl": url,
                "typeOfInfo": 'QA',
                "needUpdate": True,
                "typeOfInfo": 'QA',
                "isAnnotated": False,
                "responseAuthority": "",
                "question": pair[0],
                "answer": pair[1],
                "hasAnswer": True,
                "targetEducationLevel": 'NA',
                "topic": ["Myths"],
                "extraData": {},
                "targetLocation": "",
                "language": 'en'
            })
        return converter.write()


def main():
    scraper = WhoMythScraper(path='./', filename='WhoMyth')
    scraper.scrape()


if __name__ == '__main__':
    main()
