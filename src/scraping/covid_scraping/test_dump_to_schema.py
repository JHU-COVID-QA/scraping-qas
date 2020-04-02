import json
import uuid
import pdb

def check_keys(idx, obj):
    check_keys_v1(idx, obj)

def check_values(idx, obj):
    check_values_v1(idx, obj)

def check_keys_v1(idx, obj):
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
    assert 'sourceDate' in obj, "'sourceDate' in the %d example is missing" % idx
    return True

def check_keys_v2(idx, obj):
    assert 'sourceUrl' in obj, "'source' in the %d example is missing" % idx
    assert 'sourceName' in obj, "'sourceName' in the %d example is missing" % idx
    assert 'dateScraped' in obj, "'dateScraped' in the %d example is missing" % idx
    assert 'sourceDate' in obj, "'sourceDate' in the %d example is missing" % idx
    assert 'lastUpdateTime' in obj, "'lastUpdateTime' in the %d example is missing" % idx
    assert 'needUpdate' in obj, "'needUpdate' in the %d example is missing" % idx
    assert 'typeOfInfo' in obj, "'typeOfInfo' in the %d example is missing" % idx
    assert 'isAnnotated' in obj, "'isAnnotated' in the %d example is missing" % idx
    assert 'responseAuthority' in obj, "'responseAuthority' in the %d example is missing" % idx
    assert 'questionUUID' in obj, "'questionUUID' in the %d example is missing" % idx
    assert 'answerUUID' in obj, "'answerUUID' in the %d example is missing" % idx
    assert 'ID' in obj, "'exampleUUID' in the %d example is missing" % idx
    assert 'questionText' in obj, "'questionText' in the %d example is missing" % idx
    assert 'questionOriginal' in obj, "'questionOriginal' in the %d example is missing" % idx
    assert 'answerText' in obj, "'answerText' in the %d example is missing" % idx
    assert 'answerOriginal' in obj, "'answerOriginal' in the %d example is missing" % idx
    assert 'answerContainsURLs' in obj, "'answerContainsURLs' in the %d example is missing" % idx
    assert 'answerToks2URL' in obj, "'answerToks2URL' in the %d example is missing" % idx
    assert 'hasAnswer' in obj, "'hasAnswer' in the %d example is missing" % idx
    assert 'targetEducationLevel' in obj, "'targetEducationLevel' in the %d example is missing" % idx
    assert 'targetLocation' in obj, "'targetLocation' in the %d example is missing" % idx
    assert 'topic' in obj, "'topic' in the %d example is missing" % idx
    assert 'language' in obj, "'language' in the %d example is missing" % idx
    assert 'extraData' in obj, "'extraData' in the %d example is missing" % idx
    return True

def check_values_v1(idx, obj):
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
    assert isinstance(obj['needUpdate'], bool), "'needUpdate' in the %d example is not a boolean" % idx
    assert isinstance(obj['containsURLs'], bool), "'containsURLs' in the %d example is not a boolean" % idx
    assert isinstance(obj['typeOfInfo'], str), "'typeOfInfo' in the %d example is not a string" % idx
    assert isinstance(obj['isAnnotated'], bool), "'isAnnotated' in the %d example is not a boolean" % idx
    assert isinstance(obj['responseAuthority'], str), "'responseAuthority' in the %d example is not a string" % idx
    assert isinstance(obj['questionUUID'], str), "'questionUUID' in the %d example is not a str" % idx
    assert isinstance(uuid.UUID(obj['questionUUID']), uuid.UUID), "'questionUUID' in the %d example cannot be converted to UUID" % idx
    assert isinstance(obj['answerUUID'], str), "'answerUUID' in the %d example is not a str" % idx
    assert isinstance(uuid.UUID(obj['answerUUID']), uuid.UUID), "'answerUUID' in the %d example cannot be converted to UUID" % idx
    assert isinstance(obj['exampleUUID'], str), "'exampleUUID' in the %d example is not a str" % idx
    assert isinstance(uuid.UUID(obj['exampleUUID']), uuid.UUID), "'exampleUUID' in the %d example cannot be converted to UUID" % idx
    assert isinstance(obj['questionText'], str), "'questionText' in the %d example is not a string" % idx
    assert isinstance(obj['answerText'], str), "'answerText' in the %d example is not a string" % idx
    assert isinstance(obj['hasAnswer'], bool), "'hasAnswer' in the %d example is not a boolean" % idx
    assert isinstance(obj['targetEducationLevel'], str), "'targetEducationLevel' in the %d example is not a string" % idx
    assert isinstance(obj['topic'], str), "'topic' in the %d example is not a string" % idx
    assert isinstance(obj['extraData'], dict), "'extraData' in the %d example is not a dict" % idx
    return True

def check_values_v2(idx, obj):
    assert isinstance(obj['sourceUrl'], str), "'source' in the %d example is not a string" % idx
    assert isinstance(obj['sourceName'], str), "'sourceName' in the %d example is not a string" % idx
    assert isinstance(obj['dateScraped'], float), "'dateScraped' in the %d example is not a float" % idx
    assert isinstance(obj['needUpdate'], bool), "'needUpdate' in the %d example is not a boolean" % idx
    assert isinstance(obj['typeOfInfo'], str), "'typeOfInfo' in the %d example is not a string" % idx
    assert isinstance(obj['isAnnotated'], bool), "'isAnnotated' in the %d example is not a boolean" % idx
    assert isinstance(obj['responseAuthority'], str), "'responseAuthority' in the %d example is not a string" % idx
    assert isinstance(obj['questionUUID'], str), "'questionUUID' in the %d example is not a str" % idx
    assert isinstance(uuid.UUID(obj['questionUUID']), uuid.UUID), "'questionUUID' in the %d example cannot be converted to UUID" % idx
    assert isinstance(obj['answerUUID'], str), "'answerUUID' in the %d example is not a str" % idx
    assert isinstance(uuid.UUID(obj['answerUUID']), uuid.UUID), "'answerUUID' in the %d example cannot be converted to UUID" % idx
    assert isinstance(obj['ID'], str), "'ID' in the %d example is not a str" % idx
    assert obj['ID'].split('|||')[0] == obj['sourceName'], "'ID' in the %d example does not have sourceName as a prefix"
    assert isinstance(obj['questionOriginal'], str), "'questionOriginal' in the %d example is not a string" % idx
    assert isinstance(obj['questionText'], str), "'questionText' in the %d example is not a string" % idx
    assert isinstance(obj['answerOriginal'], str), "'questionOriginal' in the %d example is not a string" % idx
    assert isinstance(obj['answerText'], str), "'answerText' in the %d example is not a string" % idx
    assert isinstance(obj['answerContainsURLs'], bool), "'answerContainsURLs' in the %d example is not a boolean" % idx
    assert isinstance(obj['answerToks2URL'], dict), "'answerToks2URLs' in the %d example is not a dict" % idx
    assert isinstance(obj['hasAnswer'], bool), "'hasAnswer' in the %d example is not a boolean" % idx
    assert isinstance(obj['targetEducationLevel'], str), "'targetEducationLevel' in the %d example is not a string" % idx
    assert isinstance(obj['targetLocation'], str), "'targetLocation' in the %d example is not a string" % idx
    assert isinstance(obj['topic'], list), "'topic' in the %d example is not a string" % idx
    assert isinstance(obj['extraData'], dict), "'extraData' in the %d example is not a dict" % idx
    return True

def test_schema_v1(path):
    data = []
    with open(path) as fp:
        for idx, line in enumerate(fp):
            obj = json.loads(line.strip())
            if not (check_keys_v1(idx, obj) and check_values_v1(idx, obj)):
                return False
    return True


def test_schema_v2(path):
    data = []
    with open(path) as fp:
        for idx, line in enumerate(fp):
            obj = json.loads(line.strip())
            if not (check_keys_v2(idx, obj) and check_values_v2(idx, obj)):
                return False
    return True

def test_jsonlines(path, version='v0.1'):
    if 'v0.1' == version:
        return test_schema_v1(path)
    elif 'v0.2' == version:
        return test_schema_v2(path)
    else:
        print("test_jsonlines received invalid version")
        return False


if __name__ == '__main__':
    test_jsonlines("../../data/scraping/interalCOVIDinfosheet_v0.1.jsonl")
