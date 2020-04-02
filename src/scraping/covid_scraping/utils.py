# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
Utils.py

_remove_links, _clean_element, _tokenize_element borrowed directly from Darius Irani's cleaning script.
"""
__author__ = "Milind Agarwal"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Milind Agarwal"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import jsonlines
import json
from bs4 import BeautifulSoup
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
from covid_scraping.test_dump_to_schema import check_keys, check_values
from fuzzywuzzy import fuzz
import os
import time

fuzz_threshold_ques = 80
fuzz_threshold_ans = 80


# CLEANING
def _remove_links(line, field):
    nlp = English()
    if (field == 'answerText'):
        soup = BeautifulSoup(line['answerOriginal'], 'lxml')
    elif (field == 'questionText'):
        soup = BeautifulSoup(line['questionOriginal'], 'lxml')

    matcher = PhraseMatcher(line[field].vocab)

    link_dict = {}
    if soup.find('a'):
        for link in soup.find_all('a'):
            matcher = PhraseMatcher(line[field].vocab)
            matcher.add('HYPERLINK', None, *[nlp.make_doc(link.text)])
            matches = matcher(line[field])
            for _, start, end in matches:
                link_dict[str((start, end))] = link.get('href')

    fieldname = field.split('Text')[0] + 'Links'

    if (field == 'answerText'):
        line['answerToks2URL'] = link_dict
        line['answerContainsURLs'] = True
        if not bool(link_dict):
            line['answerContainsURLs'] = False


def _clean_element(line, field):
    soup = BeautifulSoup(str(line[field]), 'lxml')
    line[field] = soup.get_text().strip()


def _tokenize_element(line, field):
    """
    Opting to create tokenizer that includes English punctuation rules and exceptions.
    If tokenizer with just English vocab desired, use:
    tokenizer = Tokenizer(nlp.vocab)
    """
    nlp = English()
    tokenizer = nlp.Defaults.create_tokenizer(nlp)
    tokens = tokenizer(line[field])
    line[field] = tokens


# Example call: clean_text(listVar )
def clean_text(list_of_qa_objects):
    """Cleans a list of QA objects and returns that cleaned list of QA objects."""
    for entry in list_of_qa_objects:
        for field in ['questionText', 'answerText']:
            _clean_element(entry, field)
            _tokenize_element(entry, field)
            _remove_links(entry, field)
            entry[field] = ' '.join([token.text for token in entry[field]])

    for idx, obj in enumerate(list_of_qa_objects):
        check_keys(idx, obj)
        check_values(idx, obj)

    return list_of_qa_objects


# MERGING
# Example call: merge('../../../data/scraping/schema_v0.2/AVMA_v0.2.jsonl', listVar )
def merge(gold_jsonl_path, list_of_qa_objects):
     """
     Uses fuzzy matching on the questions and answers from a list of QA objects to merge with an existing JSONL file.
     
     Parameters:
     1. gold_jsonl_path: path to the gold JSONL file
     2. list_of_qa_objects: a list of JSON type QA objects produced after rescraping and cleaning.
     
     Returns:
        goldData: modified list of JSON type QA objects after merge
     """
    goldData = []
    goldQues = []
    with jsonlines.open(gold_jsonl_path) as q:
        for line in q.iter():
            goldData.append(line)
            goldQues.append(line['questionText'])

    for entry in list_of_qa_objects:
        ques = entry['questionText']
        ans = entry['answerText']

        def fuzzy_PR_ques(x): return fuzz.partial_ratio(ques, x)

        goldQuesScores = list(map(fuzzy_PR_ques, goldQues))
        found = (sum(i >= fuzz_threshold_ques for i in goldQuesScores) > 0)
        if not found:
            # print('Not found. Adding this json object to the gold data')
            goldData.append(entry)

        else:
            maxix = goldQuesScores.index(max(goldQuesScores))
            goldA = goldData[maxix]['answerText']
            ansScore = fuzz.partial_ratio(ans, goldA)

            # check if the new answer matches the existing answer for
            # that question:
            if ansScore > fuzz_threshold_ans:
                # print('Answer match found. Updating metadata')
                goldData[maxix]['dateScraped'] = time.time()
                goldData[maxix]['lastUpdateTime'] = time.time()

            else:
                # print('Answer match NOT found. Updating answer and metadata.')
                goldData[maxix]['answerText'] = ans
                goldData[maxix]['answerUUID'] = entry['answerUUID']
                goldData[maxix]['dateScraped'] = time.time()
                goldData[maxix]['lastUpdateTime'] = time.time()
                goldData[maxix]['hasAnswer'] = True

    return goldData
