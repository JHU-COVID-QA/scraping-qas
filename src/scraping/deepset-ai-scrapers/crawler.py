# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
COVID-QA crawler
This script runs a series crawlers written by deepset-ai.
Here is link to their work.
https://github.com/deepset-ai/COVID-QA/tree/master/datasources/scrapers
"""
__author__ = "Max Fleming"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Max Felming"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

from os import listdir
from os.path import isfile, join
import subprocess
import re
import json
import uuid
import time
import jsonlines

from test_dump_to_schema import test_jsonlines

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--rescrape", action='store_true')
args = parser.parse_args()
diff = ''
extension = ''
if args.rescrape:
    diff = 'stage/'
    extension = '_STAGE'


def scrap():
    onlyfiles = [f for f in listdir('.') if isfile(join('.', f))]
    for file in onlyfiles:
        if 'scraper' in file:
            faq = []
            subprocess.call(['scrapy', 'runspider', file, '-o', 'tmp.json'])
            with open('tmp.json') as json_file:
                data = json.load(json_file)[0]
                for i in range(len(data['question'])):
                    faq.append({
                        'sourceUrl': data['link'][i],
                        'sourceName': data['source'][i],
                        "dateScraped": time.time(),
                        "sourceDate": None,
                        "lastUpdateTime": None,
                        "needUpdate": True,
                        "containsURLs": 'http' in data['answer'][i],
                        "typeOfInfo": "QA",
                        "isAnnotated": False,
                        "responseAuthority": "",
                        "questionUUID": str(uuid.uuid1()),
                        "answerUUID": str(uuid.uuid1()),
                        "exampleUUID": str(uuid.uuid1()),
                        "questionText": data['question'][i],
                        "answerText": data['answer'][i],
                        "hasAnswer": True,
                        "targetEducationLevel": "NA",
                        "topic": "",
                        "extraData": {
                            'country': data['country'][i],
                            'region': data['region'][i],
                            'city': data['region'][i],
                            'lang': data['lang'][i]
                        },
                    })
            subprocess.call(['rm', 'tmp.json'])
            with jsonlines.open('../../../data/scraping/schema_v0.1/' + diff + file.split('_scraper')[0] + '_v0.1' + extension + '.jsonl', 'w') as writer:
                writer.write_all(faq)
            test_jsonlines(
                '../../../data/scraping/schema_v0.1/' +
                diff +
                file.split('_scraper')[0] +
                '_v0.1' +
                extension +
                '.jsonl')


def main():
    scrap()


if __name__ == "__main__":
    main()
