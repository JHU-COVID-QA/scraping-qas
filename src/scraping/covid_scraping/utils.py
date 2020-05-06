# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
Utils.py
_remove_links, _clean_element, _tokenize_element borrowed directly from Darius Irani's cleaning script.
"""
__author__ = "Milind Agarwal, Adam Poliak"
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
from fuzzywuzzy import fuzz
import os
import time
import uuid
import warnings

fuzz_threshold_ques = 80
fuzz_threshold_ans = 80


# CLEANING
def _remove_links(str, tokens):
    nlp = English()
    soup = BeautifulSoup(str, 'lxml')
    matcher = PhraseMatcher(tokens.vocab)
    link_dict = {}
    if soup.find('a'):
        for link in soup.find_all('a'):
            matcher = PhraseMatcher(tokens.vocab)
            matcher.add('HYPERLINK', None, *[nlp.make_doc(link.text)])
            matches = matcher(str)
            for _, start, end in matches:
                link_dict[str((start, end))] = link.get('href')
    return link_dict


def _clean_element(str):
    return BeautifulSoup(str, 'lxml').get_text().strip()


def _tokenize_element(str):
    """
    Opting to create tokenizer that includes English punctuation rules and exceptions.
    If tokenizer with just English vocab desired, use:
    tokenizer = Tokenizer(nlp.vocab)
    """
    nlp = English()
    tokenizer = nlp.Defaults.create_tokenizer(nlp)
    return tokenizer(str)


# Example call: clean_text(str)
def clean_text(string, tokenize=False):
    """
    Cleans a html str and returns clean str and tokenized links.
    """
    string = _clean_element(string)
    if tokenize:
        tokens = _tokenize_element(string)
        link_dict = _remove_links(string, tokens)
        return ' '.join(token.text for token in tokens), link_dict
    else:
        return string, {}


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
    try:
        with jsonlines.open(gold_jsonl_path) as q:
            for line in q.iter():
                goldData.append(line)
                goldQues.append(line['questionText'])
    except:
        warnings.warn("File not found when for merging " + str(list_of_qa_objects[0]['sourceName'])+ ". This should only happen on the first time the scraper is run", UserWarning ,stacklevel=4)
    for entry in list_of_qa_objects:
        ques = entry['questionText']
        ans = entry['answerText']

        def fuzzy_PR_ques(x): return fuzz.partial_ratio(ques, x)

        goldQuesScores = list(map(fuzzy_PR_ques, goldQues))
        found = (sum(i >= fuzz_threshold_ques for i in goldQuesScores) > 0)
        if not found:
            # print('Not found. Adding this json object to the gold data')
            goldData.append(entry)
            # When an new entry is found it needs to be assigned question/answer/example UUIDs
            goldData[-1]['questionUUID'] = str(uuid.uuid1())
            goldData[-1]['answerUUID'] = str(uuid.uuid1())
            goldData[-1]['exampleUUID'] = str(uuid.uuid1())



        else:
            maxix = goldQuesScores.index(max(goldQuesScores))
            goldA = goldData[maxix]['answerText']
            ansScore = fuzz.partial_ratio(ans, goldA)
            #Updating the time stamps
            goldData[maxix]['dateScraped'] = entry['dateScraped']
            goldData[maxix]['lastUpdateTime'] = entry['lastUpdateTime']
            goldData[maxix]['sourceDate'] = entry['sourceDate']

            # check if the new answer matches the existing answer for
            # that question:
            if ansScore <= fuzz_threshold_ans:
                # print('Answer match NOT found. Updating answer and metadata.')
                goldData[maxix]['answerText'] = ans
                goldData[maxix]['hasAnswer'] = True
                #When a answer is changed it needs a new answer/example UUID
                goldData[maxix]['answerUUID'] = str(uuid.uuid1())
                goldData[maxix]['exampleUUID'] = str(uuid.uuid1())

    return goldData


def remove_unanswered_examples(input_f, output_f):
    """
    Creates a new jsonl that only includes questions that have answers"

    Parameters:
    1. input_f:  jsonl file with questions and answers
    2. output_f: new jsonl file with just questions
    These files must be different
    """
    if input_f == output_f:
        raise Exception("The input and output files are the same, they need to be different")
    output_data = []
    with jsonlines.open(input_f) as q:
        for line in q.iter():
            if line['hasAnswer']:
                output_data.append(line)

    with jsonlines.open(output_f, 'w') as writer:
        writer.write_all(output_data)
    # TODO: add logging that logs how many examples were removed
