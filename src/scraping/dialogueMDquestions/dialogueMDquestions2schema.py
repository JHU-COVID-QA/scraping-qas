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
  for line in open("translated_questions.txt"):
    data.append(to_schema(line.strip()))

  with jsonlines.open('../../../data/scraping/translatedDialogueMDquestions_v0.1.jsonl', 'w') as writer:
    writer.write_all(data)

  test_jsonlines('../../../data/scraping/translatedDialogueMDquestions_v0.1.jsonl')

if __name__ == '__main__':
  main()
