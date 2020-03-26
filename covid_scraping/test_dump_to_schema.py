import json
import uuid
import pdb

def check_keys(idx, obj):
  assert 'topic' in obj, "'topic' in the %d example is missing" % idx
  assert 'sourceUrl' in obj, "'source' in the %d example is missing" % idx
  assert 'sourceName' in obj, "'sourceName' in the %d example is missing" % idx
  assert 'dateScraped' in obj, "'dateScraped' in the %d example is missing" % idx
  assert 'lastUpdateTime' in obj, "'lastUpdateTime' in the %d example is missing" % idx
  assert 'needUpdate' in obj, "'needUpdate' in the %d example is missing" % idx
  assert 'containsURLs' in obj, "'containsURLs' in the %d example is missing" % idx
  assert 'typeOfInfo' in obj, "'typeOfInfo' in the %d example is missing" % idx
  assert 'isAnnotated' in obj, "'isAnnotated' in the %d example is missing" % idx
  assert 'responseAuthority' in obj, "'responseAuthority' in the %d example is missing" % idx
  assert 'questionUUID' in obj, "'questionUUID' in the %d example is missing" % idx
  assert 'answerUUID' in obj, "'answerUUID' in the %d example is missing" % idx
  assert 'exampleUUID' in obj, "'exampleUUID' in the %d example is missing" % idx
  assert 'questionText' in obj, "'questionText' in the %d example is missing" % idx
  assert 'answerText' in obj, "'answerText' in the %d example is missing" % idx
  assert 'hasAnswer' in obj, "'hasAnswer' in the %d example is missing" % idx
  assert 'targetEducationLevel' in obj, "'targetEducationLevel' in the %d example is missing" % idx
  assert 'topic' in obj, "'topic' in the %d example is missing" % idx
  assert 'extraData' in obj, "'extraData' in the %d example is missing" % idx

def check_values(idx, obj):
  '''
  sourceUrl: Url for the source
  sourceName: name of the source (CDC, JHU, NYtimes, etc)
  dateScraped: POSIX time of what the data was scraped
  sourceDate: POSIX time of when this data was published
  lastUpdateTime (last time the story was updated): POSIX time
  needUpdate (does this need to be updated or is it static information): boolean
  containsURLs (does this contain urls): boolean
  typeOfInfo: QA, Fact, Opinion, etc?
  isAnnotated: boolean
  responseAuthority: str (if it is at JHU to know who the answer came from)
  questionUUID: UUID (stored as a string)
  answerUUID: UUID (stored as a string)
  exampleUUID: UUID (stored as a string)
  questionText: str
  answerText: str
  hasAnswer? boolean
  targetEducationLevel: "Elementary", "HS", "College", "NA"
  topic: str
  extraData (this contains any extra data that you think is useful): dictionary
  '''
  assert isinstance(obj['topic'], str), "'topic' in the %d example is not a string" % idx
  assert isinstance(obj['sourceUrl'], str), "'source' in the %d example is not a string" % idx
  assert isinstance(obj['sourceName'], str), "'sourceName' in the %d example is not a string" % idx
  assert isinstance(obj['dateScraped'], float), "'dateScraped' in the %d example is not a float" % idx
  #assert isinstance(uuid.UUID(obj['dateScraped']), uuid.UUID), "'dateScraped' in the %d example cannot be converted to UUID" % idx
  #assert isinstance(obj['lastUpdateTime'], float), "'lastUpdateTime' in the %d example is not a float" % idx
  assert isinstance(obj['needUpdate'], bool),  "'needUpdate' in the %d example is not a boolean" % idx
  assert isinstance(obj['containsURLs'], bool),  "'containsURLs' in the %d example is not a boolean" % idx
  assert isinstance(obj['typeOfInfo'], str), "'typeOfInfo' in the %d example is not a string" % idx
  assert isinstance(obj['isAnnotated'], bool),  "'isAnnotated' in the %d example is not a boolean" % idx
  assert isinstance(obj['responseAuthority'], str), "'responseAuthority' in the %d example is not a string" % idx
  assert isinstance(obj['questionUUID'], str), "'questionUUID' in the %d example is not a str" % idx
  assert isinstance(uuid.UUID(obj['questionUUID']), uuid.UUID), "'questionUUID' in the %d example cannot be converted to UUID" % idx
  assert isinstance(obj['answerUUID'], str), "'answerUUID' in the %d example is not a str" % idx
  assert isinstance(uuid.UUID(obj['answerUUID']), uuid.UUID), "'answerUUID' in the %d example cannot be converted to UUID" % idx
  assert isinstance(obj['exampleUUID'], str), "'exampleUUID' in the %d example is not a str" % idx
  assert isinstance(uuid.UUID(obj['exampleUUID']), uuid.UUID), "'exampleUUID' in the %d example cannot be converted to UUID" % idx
  assert isinstance(obj['questionText'], str), pdb.set_trace() #"'questionText' in the %d example is not a string" % idx
  assert isinstance(obj['answerText'], str), "'answerText' in the %d example is not a string" % idx
  assert isinstance(obj['hasAnswer'], bool),  "'hasAnswer' in the %d example is not a boolean" % idx
  assert isinstance(obj['targetEducationLevel'], str), "'targetEducationLevel' in the %d example is not a string" % idx
  assert isinstance(obj['topic'], str), "'topic' in the %d example is not a string" % idx
  assert isinstance(obj['extraData'], dict), "'extraData' in the %d example is not a dict" % idx

def test_jsonlines(path):
  data = []
  for line in open(path):
    data.append(json.loads(line.strip()))

  for idx, obj in enumerate(data):
    check_keys(idx, obj)
    check_values(idx, obj)

  print("Passed!!")



if __name__ == '__main__':
  test_jsonlines("../../data/scraping/interalCOVIDinfosheet_v0.1.jsonl")


