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
from covid_scraping import utils, test_jsonlines


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
                                        'typeOfInfo',
                                        'isAnnotated',
                                        'responseAuthority',
                                        'hasAnswer',
                                        'targetEducationLevel',
                                        'extraData']
        v1_requirements_from_conversion = ['dateScraped',
                                           'questionText',
                                           'answerText',
                                           'containsURLs',
                                           'questionUUID',
                                           'answerUUID',
                                           'exampleUUID',
                                           'topic']
        path = '../../../data/scraping/schema_v0.1/' + self._file_prefix + '_v0.1.jsonl'
        qas = []
        with jsonlines.open(path, mode='w') as writer:
            for example in self._examples:
                questionText, question_link_dict = utils.clean_text(example['question'])
                answerText, answer_link_dict = utils.clean_text(example['answer'])
                pairs_from_scraper = dict(zip(v1_requirements_from_scraper, list(map(example.get, v1_requirements_from_scraper))))
                v1_conversion = [time.time(),
                                 questionText,
                                 answerText,
                                 bool(answer_link_dict),
                                 str(uuid.uuid1()),
                                 str(uuid.uuid1()),
                                 str(uuid.uuid1()),
                                 example['topic'][0] if example['topic'] else ""]
                pairs_from_conversion = dict(zip(v1_requirements_from_conversion, v1_conversion))
                qas.append({**pairs_from_scraper, **pairs_from_conversion})
        gold_data = utils.merge(path, qas)
        with jsonlines.open(path, 'w') as writer:
            writer.write_all(gold_data)
        test_jsonlines(path, 'v0.1')

    def writeV2(self):
        v2_requirements_from_scraper = ['sourceUrl',
                                        'sourceName',
                                        'sourceDate',
                                        'lastUpdateTime',
                                        'needUpdate',
                                        'typeOfInfo',
                                        'isAnnotated',
                                        'responseAuthority',
                                        'hasAnswer',
                                        'targetEducationLevel',
                                        'targetLocation',
                                        'language',
                                        'extraData',
                                        'topic']
        v2_requirements_from_conversion = ['dateScraped',
                                           'questionOriginal',
                                           'questionText',
                                           'answerOriginal',
                                           'answerText',
                                           'questionUUID',
                                           'answerUUID',
                                           'ID',
                                           'answerContainsURLs',
                                           'answerToks2URL']
        path = '../../../data/scraping/schema_v0.2/' + self._file_prefix + '_v0.2.jsonl'
        qas = []
        with jsonlines.open(path, mode='w') as writer:
                for example in self._examples:
                    questionText, question_link_dict = utils.clean_text(example['question'])
                    answerText, answer_link_dict = utils.clean_text(example['answer'])
                    pairs_from_scraper = dict(zip(v2_requirements_from_scraper, list(map(example.get, v2_requirements_from_scraper))))
                    v2_conversion = [time.time(),
                                     example['question'],
                                     questionText,
                                     example['answer'],
                                     answerText,
                                     str(uuid.uuid1()),
                                     str(uuid.uuid1()),
                                     example['sourceName'] + '|||' + str(hash(str(example['question']))),
                                     bool(answer_link_dict),
                                     answer_link_dict]
                    pairs_from_conversion = dict(zip(v2_requirements_from_conversion, v2_conversion))
                    qas.append({**pairs_from_scraper, **pairs_from_conversion})
        gold_data = utils.merge(path, qas)
        with jsonlines.open(path, 'w') as writer:
            writer.write_all(gold_data)
        test_jsonlines(path, 'v0.2')

    def write(self):
        self.writeV1()
        self.writeV2()
