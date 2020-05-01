# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.

__author__ = "Max Fleming, Darius Irani"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Max Fleming"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import jsonlines
import time
from bs4 import BeautifulSoup
from covid_scraping import utils, test_jsonlines


class Conversion():
    def __init__(self, file_prefix, path, dateScraped, lastUpdateTime):
        """
        This is the constructor for Conversion, the file_prefix should be the name
        of the file you want i.e. if your scraping 'American Veterinarian
        Medical Association', and approptiate file prefix would be 'AVMA'.
        The path should be the path from the directory your working in to
        Covid-19-infobot/data/scraping
        """
        self._examples = []
        self._file_prefix = file_prefix
        self._path = path
        self._dateScraped = dateScraped
        self._lastUpdateTime = lastUpdateTime

    def _check_example(self, example):
        required_keys_to_type = {'sourceUrl': str,
                                 'sourceName': str,
                                 'needUpdate': bool,
                                 'typeOfInfo': str,
                                 'isAnnotated': bool,
                                 'responseAuthority': str,
                                 'question': str,
                                 'answer': str,
                                 'hasAnswer': bool,
                                 'targetEducationLevel': str,
                                 'topic': list,
                                 'extraData': dict,
                                 'targetLocation': str,
                                 'language': str}
        for key in required_keys_to_type.keys():
            if key not in example:
                raise KeyError("'" + key + "'" + "was not found in dictionary")
            if not isinstance(example[key], required_keys_to_type[key]):
                raise ValueError("'" +
                                 key +
                                 "'" +
                                 "should be type " +
                                 str(required_keys_to_type[key]))
        for field in ['question', 'answer']:
            if len(example[field].strip()) == 0:  # indicates empty field
                raise ValueError('{} field is empty'.format(field))

    def addExample(self, dict):
        """
        Added a qa pair to the converter the dictionary pass should have the
        following fields
        sourceUrl
        sourceName
        sourceDate
        lastUpdateTime
        needUpdate
        typeOfInfo
        isAnnotated
        responseAuthority
        question
        answer
        hasAnswer
        targetEducationLevel
        topic
        extraData
        targetLocation
        language
        """
        self._check_example(dict)
        self._examples.append(dict)

    def _writeV2(self):
        v2_requirements_from_scraper = ['sourceUrl',
                                        'sourceName',
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
        v2_requirements_from_conversion = ['sourceDate',
                                           'lastUpdateTime',
                                           'dateScraped',
                                           'questionOriginal',
                                           'questionText',
                                           'answerOriginal',
                                           'answerText',
                                           'ID',
                                           'answerContainsURLs',
                                           'answerToks2URL']
        path = self._path + '/schema_v0.2/' + self._file_prefix + '_v0.2.jsonl'
        qas = []
        for example in self._examples:
            questionText, question_link_dict = utils.clean_text(
                example['question'])
            answerText, answer_link_dict = utils.clean_text(example['answer'])
            pairs_from_scraper = dict(zip(v2_requirements_from_scraper, list(
                map(example.get, v2_requirements_from_scraper))))
            v2_conversion = [self._lastUpdateTime,
                             self._lastUpdateTime,
                             self._dateScraped,
                             example['question'],
                             questionText,
                             example['answer'],
                             answerText,
                             example['sourceName'] + '|||' + str(hash(str(example['question']))),
                             bool(answer_link_dict),
                             answer_link_dict]
            pairs_from_conversion = dict(
                zip(v2_requirements_from_conversion, v2_conversion))
            qas.append({**pairs_from_scraper, **pairs_from_conversion})
        gold_data = utils.merge(path, qas)
        # Merging could add a exampleUUID for a new example.
        for example in gold_data:
            example.pop('exampleUUID', None)
        with jsonlines.open(path, 'w') as writer:
            writer.write_all(gold_data)
        return test_jsonlines(path, 'v0.2')

    def write(self):
        "Write all the added examples to the paths specified in the constructor"
        return self._writeV2()
