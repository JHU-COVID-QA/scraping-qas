# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
DialogueMD Questions crawler
Expected page to crawl is 
translated_questions.txt
"""
__author__ = "Adam Poliak"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Adam Poliak"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import pandas as pd
import uuid
import jsonlines
import time

from covid_scraping import test_jsonlines

def to_schema(question):
  # ['Question', 'Answer', 'Need to update (Y/N)', 'Tags', 'Author']
  # Question  Answer  Need to update (Y/N)  Tags  Source  Annotator/Author
  data = {
    "sourceUrl": "",
    "sourceName": "translatedDialogueMDquestions",
    "dateScraped": time.time(),
    "sourceDate": time.time(),
    "lastUpdateTime": time.time(),
    "needUpdate": True,
    "containsURLs": False, #need to make this programmitic
    "typeOfInfo": "QA",
    "isAnnotated": False,
    "responseAuthority": "",
    "questionUUID": str(uuid.uuid1()),
    "answerUUID": str(uuid.uuid1()),
    "exampleUUID": str(uuid.uuid1()),
    "questionText": question,
    "answerText": "",
    "hasAnswer": False,
    "targetEducationLevel": "NA",
    "topic": "",
    "extraData": {
    }
  }
  return data

def main():
  data = []
  question_set = set()
  for line in open("translated_questions.txt"):
    question_set.add(line.strip())
  for line in open("translated_questions1.txt"):
    question_set.add(line.strip())

  for question in question_set:
    data.append(to_schema(question))

  with jsonlines.open('../../../data/scraping/translatedDialogueMDquestions_v0.1.jsonl', 'w') as writer:
    writer.write_all(data)

  test_jsonlines('../../../data/scraping/translatedDialogueMDquestions_v0.1.jsonl')

if __name__ == '__main__':
  main()
