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
import json
import uuid
import re
import argparse
import requests
import os
from bs4 import BeautifulSoup, NavigableString, CData, Tag
from datetime import datetime as dt
from collections import namedtuple
from covid_scraping import test_jsonlines


class Schema():
    def __init__(self, topic, sourcedate, contain_url,
                 response_auth, question, answer, extradata):
        self.timestamp_ = int(time.mktime(dt.now().timetuple()))
        self.sourcedate_ = sourcedate
        self.contain_url_ = contain_url
        self.response_auth_ = response_auth
        self.question_ = question
        self.answer_ = answer
        self.extradata_ = extradata

        topic['sourceName'] = 'CNN'
        topic['typeOfInfo'] = 'QA'
        topic['dateScraped'] = float(self.timestamp_)
        topic['sourceDate'] = self.sourcedate_
        topic['lastUpdateTime'] = self.sourcedate_
        topic['needUpdate'] = True
        topic['containsURLs'] = contain_url
        topic['isAnnotated'] = False
        # str (if it is at JHU to know who the answer came from)
        topic['responseAuthority'] = self.response_auth_
        topic['questionUUID'] = str(uuid.uuid1())
        topic['answerUUID'] = str(uuid.uuid1())
        topic['exampleUUID'] = str(uuid.uuid1())
        topic['questionText'] = self.question_
        topic['answerText'] = self.answer_
        topic['hasAnswer'] = True
        topic['targetEducationLevel'] = 'NA'
        topic['extraData'] = self.extradata_


class Crawler():
    def __init__(self, url, datadir, filename):
        self.url = url
        self.response_auth = 'CNN'
        self.sourcedate = self.get_date(url)
        self.datadir = datadir
        self.filename = filename

    def get_date(self, url):
        date_dict = {'january': '1', 'february': '2', 'march': '3', 'april': '4', 'may': '5', 'june': '6',
                     'july': '7', 'august': '8', 'september': '9', 'october': '10', 'november': '11', 'december': '12'}

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        sourcedate = soup.find(
            'div', class_='cnnix-timestamp').get_text().split()[1:]
        sourcedate = sourcedate
        month = sourcedate[0].lower()
        if month in date_dict:
            month = date_dict[month]
        else:
            return 'NA'
        day = sourcedate[1].split(',')[0]
        year = sourcedate[2]
        sourcedate = dt(int(year), int(month), int(day), 0, 0).timestamp()
        return sourcedate

    def scrape(self):
        Schema = namedtuple('Schema', 'question answer extra_data')
        Block = namedtuple('Block', 'content tags')
        extra_data = {}

        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        tags = [tag.get('data-topic')
                for tag in soup.find_all('div', attrs={'class': 'nav-button'})]

        body = soup.find_all(
            'div', attrs={
                'class': 'interactive-container'})[1]
        blocks = []
        for div in body.find_all('div'):
            if 'question' == div.get('class')[0]:
                tags = ','.join(div.get('class')[1:])
                block = Block(div, tags)
                blocks.append(block)

        questions = []
        answers = []
        extra_data_ = []
        for block in blocks:
            question = block.content.find('div', attrs={'class': 'question-q'})
            answer = block.content.find('div', attrs={'class': 'question-a'})
            if answer.find('a'):
                links = [(link.text, link.get('href'))
                         for link in answer.find_all('a')]
                extra_data[question.get_text()] = links
            extra_data['Tag: ' + question.get_text()] = block.tags
            questions.append(question.get_text())
            answers.append(answer.get_text())
            extra_data_.append(extra_data)

        schema = Schema(questions, answers, extra_data_)
        self.dump(schema)

    def dump(self, schema):
        with open(os.path.join(self.datadir, self.filename), 'w') as writer:
            for question, answer, extra_data in zip(
                    schema.question, schema.answer, schema.extra_data):
                topic = {
                    'topic': 'Top Coronavirus Questions',
                    'sourceUrl': self.url}
                contain_url = question in extra_data
                Schema(
                    topic,
                    self.sourcedate,
                    contain_url,
                    self.response_auth,
                    question,
                    answer,
                    extra_data)
                json.dump(topic, writer)
                writer.write('\n')


def get_args():
    parser = argparse.ArgumentParser(
        description="Scrape resources from Medicaid.")
    parser.add_argument(
        '--url',
        help='CNN COVID QA url',
        type=str,
        default='https://www.cnn.com/interactive/2020/health/coronavirus-questions-answers/')
    parser.add_argument(
        '--datadir',
        help='data directory',
        type=str,
        default='./')
    parser.add_argument(
        '--filename',
        help='jsonl filename',
        type=str,
        default='CNN_v0.1.jsonl')
    parser.add_argument("--rescrape", action='store_true')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()

    diff = ''
    extension = ''
    if args.rescrape:
        diff = 'stage/'
        extension = '_STAGE'

    crw = Crawler(
        args.url,
        args.datadir +
        diff,
        args.filename.split('.jsonl')[0] +
        extension +
        '.jsonl')
    crw.scrape()
    test_jsonlines(
        os.path.join(
            args.datadir +
            diff,
            args.filename.split('.jsonl')[0] +
            extension +
            '.jsonl'))
