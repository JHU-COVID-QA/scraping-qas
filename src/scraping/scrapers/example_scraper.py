# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.

__author__ = "Adam Poliak"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Adam Poliak"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

from covid_scraping import Scraper
from covid_scraping import Conversion, test_jsonlines
import random
import time


class ExampleScraper(Scraper):
    """Scrapers a website for FAQs and stores the output to a file"""

    def scrape(self):
        converter = Conversion(
            self._filename,
            self._path,
            self._dateScraped,
            time.time())
        # Put the code here that makes the
        for exampleNums in range(10):
            converter.addExample({
                'sourceUrl': 'example.com',
                'sourceName': "example",
                "needUpdate": True,
                "typeOfInfo": "QA",
                "isAnnotated": False,
                "responseAuthority": "",
                "question": '<a href="example.com/dir1">What is COVID-19?</a>',
                "answer": '<p><a href="example.com/dir2">Coronaviruses</a> are a large family of viruses.</p>',
                "hasAnswer": True,
                "targetEducationLevel": "NA",
                "topic": ['topic1', 'topic2'],
                "extraData": {'hello': 'goodbye'},
                "targetLocation": "US",
                "language": 'en',
            })
        # This write() will fail because the path doesnt exist
        return converter.write()


def main():
    scraper = ExampleScraper(path="./", filename="example")
    scraper.scrape()


if __name__ == '__main__':
    main()
