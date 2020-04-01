# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.

__author__ = "Max Fleming"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Max Fleming"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import jsonlines
import time
import uuid
from bs4 import BeautifulSoup
from covid_scraping import test_jsonlines
from .clean_jsonl import *

def _has_links(answer):
    return bool(answer.find('a'))

def _map_links(answer):
    link_dict = {}
    if answer.find('a'):
        for link in answer.find_all('a'):
            link_dict[link.get_text().strip()] = link.get('href')
    return link_dict

class Conversion():
    def __init__(self, file_prefix):
        self._examples = []
        self._file_prefix = file_prefix


    def addExample(self, dict):
        self._examples.append(dict)


    def writeV1(self):
        v1_requirements_from_scraper = ['sourceUrl',
                                        'sourceName',
                                        'sourceDate',
                                        'lastUpdateTime',
                                        'needUpdate',
                                        'containsURLs',
                                        'typeOfInfo',
                                        'isAnnotated',
                                        'responseAuthority',
                                        'hasAnswer',
                                        'targetEducationLevel',
                                        'extraData']
        v1_requirements_from_conversion = ['dateScraped',
                                           'questionText',
                                           'answerText',
                                           'questionUUID',
                                           'answerUUID',
                                           'exampleUUID',
                                           'topic']
        path = '../../../data/scraping/schema_v0.1/' + self._file_prefix + '_v0.1.jsonl'
        with jsonlines.open(path, mode='w') as writer:
            for example in self._examples:
                pairs_from_scraper = dict(zip(v1_requirements_from_scraper, list(map(example.get, v1_requirements_from_scraper))))
                pairs_from_conversion = dict(zip(v1_requirements_from_conversion, [time.time(), str(example['question']), str(example['answer']), str(uuid.uuid1()), str(uuid.uuid1()), str(uuid.uuid1()), example['topicV1']]))
                writer.write({**pairs_from_scraper, **pairs_from_conversion})
        clean_jsonl(path)
        test_jsonlines(path)

    def writeV2(self):
        v2_requirements_from_scraper = ['sourceUrl',
                                        'sourceName',
                                        'sourceDate',
                                        'lastUpdateTime',
                                        'needUpdate',
                                        'containsURLs',
                                        'typeOfInfo',
                                        'isAnnotated',
                                        'responseAuthority',
                                        'hasAnswer',
                                        'targetEducationLevel',
                                        'targetLocation',
                                        'language',
                                        'extraData']
        v2_requirements_from_conversion = ['dateScraped',
                                           'questionOriginal',
                                           'questionText',
                                           'answerOriginal',
                                           'answerText',
                                           'questionUUID',
                                           'answerUUID',
                                           'ID',
                                           'answerContainsURLs',
                                           'answerToks2URL',
                                           'topic']
        path = '../../../data/scraping/schema_v0.2/' + self._file_prefix + '_v0.2.jsonl'
        with jsonlines.open(path, mode='w') as writer:
                for example in self._examples:
                    pairs_from_scraper = dict(zip(v2_requirements_from_scraper, list(map(example.get, v2_requirements_from_scraper))))
                    v2_conversion = [time.time(),
                                     str(example['question']),
                                     example['question'].get_text().strip(),
                                     str(example['answer']),
                                     example['answer'].get_text().strip() if example['hasAnswer'] else "",
                                     str(uuid.uuid1()),
                                     str(uuid.uuid1()),
                                     example['sourceName'] + '|||' + str(hash(str(example['question']))),
                                     _has_links(example['answer']) if example['hasAnswer'] else False,
                                     _map_links(example['answer']) if example['hasAnswer'] else {},
                                     example['topicV2']]
                    pairs_from_conversion = dict(zip(v2_requirements_from_conversion, v2_conversion))
                    writer.write({**pairs_from_scraper, **pairs_from_conversion})


    def write(self):
        self.writeV1()
        self.writeV2()
