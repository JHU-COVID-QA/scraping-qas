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
from covid_scraping import utils
from .test_dump_to_schema import test_jsonlines

def _has_links(original):
    return bool(BeautifulSoup(original, 'lxml').find('a'))


def _correct_fields(qa_pair):
    qa_pair['extraData']['questionOriginal'] = qa_pair['questionOriginal']
    qa_pair['extraData']['answerOriginal'] = qa_pair['answerOriginal']
    qa_pair.pop('questionOriginal')
    qa_pair.pop('answerOriginal')


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
                pairs_from_scraper = dict(zip(v1_requirements_from_scraper, list(map(example.get, v1_requirements_from_scraper))))
                v1_conversion = [time.time(),
                                 str(example['question']),
                                 str(example['answer']),
                                 _has_links(example['answer']) if example['hasAnswer'] else False,
                                 str(uuid.uuid1()),
                                 str(uuid.uuid1()),
                                 str(uuid.uuid1()),
                                 example['topic'][0] if example['topic'] else ""]
                pairs_from_conversion = dict(zip(v1_requirements_from_conversion, v1_conversion))
                qas.append({**pairs_from_scraper, **pairs_from_conversion, 'questionOriginal': example['question'], 'answerOriginal': example['answer']})
        qas = utils.clean_text(qas)
        for qa in qas:
            _correct_fields(qa)
        gold_data = utils.merge(path, qas)
        with jsonlines.open(path, 'w') as writer:
            writer.write_all(gold_data)
        test_jsonlines(path)

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
                                           'ID']
        # v2 requirements from cleaning : answerContainsURLs answerToks2URL
        path = '../../../data/scraping/schema_v0.2/' + self._file_prefix + '_v0.2.jsonl'
        qas = []
        with jsonlines.open(path, mode='w') as writer:
                for example in self._examples:
                    pairs_from_scraper = dict(zip(v2_requirements_from_scraper, list(map(example.get, v2_requirements_from_scraper))))
                    v2_conversion = [time.time(),
                                     example['question'],
                                     #cleaning will fill questionText correctly
                                     example['question'],
                                     example['answer'],
                                     #cleaing will will in answerText corrctly
                                     example['answer'],
                                     str(uuid.uuid1()),
                                     str(uuid.uuid1()),
                                     example['sourceName'] + '|||' + str(hash(str(example['question'])))]
                    pairs_from_conversion = dict(zip(v2_requirements_from_conversion, v2_conversion))
                    qas.append({**pairs_from_scraper, **pairs_from_conversion})
        gold_data = utils.merge(path, utils.clean_text(qas))
        with jsonlines.open(path, 'w') as writer:
            writer.write_all(gold_data)
        test_jsonlines(path)


    def write(self):
        self.writeV1()
        self.writeV2()
