from covid_scraping import Conversion
import subprocess
import jsonlines
from test_dump_to_schema import test_jsonlines


def test_init():
    converter = Conversion('test')
    assert converter._file_prefix is 'test'
    assert isinstance(converter._examples, list)


def test_addExample():
    converter = Conversion('test')
    converter.addExample({
        'sourceUrl': 'example.com',
        'sourceName': "example",
        "sourceDate": 1585777414.515401,
        "lastUpdateTime": 1585777414.515401,
        "needUpdate": True,
        "typeOfInfo": "QA",
        "isAnnotated": False,
        "responseAuthority": "",
        "question": '<a href="example.com/dir1">What is COVID-19?</a>',
        "answer": '<p><a href="example.com/dir2">Coronaviruses</a> are a large family of viruses.</p>',
        "hasAnswer": True,
        "targetEducationLevel": "NA",
        "topic": ['topic1', 'topic2'],
        "extraData": {'hello': 'goodbye'},
        "targetLocation": "US",
        "language": 'en',
    })
    converter.write()


def test_schema_v01():
    test_jsonlines('../../../data/scraping/schema_v0.1/test_v0.1.jsonl')
    with jsonlines.open('../../../data/scraping/schema_v0.1/test_v0.1.jsonl', 'r') as reader:
        line = reader.read()
        assert line['questionText'] == 'What is COVID-19 ?'
        assert line['answerText'] == 'Coronaviruses are a large family of viruses .'


def test_schema_v02():
    test_jsonlines('../../../data/scraping/schema_v0.2/test_v0.2.jsonl')
    with jsonlines.open('../../../data/scraping/schema_v0.2/test_v0.2.jsonl', 'r') as reader:
        line = reader.read()
        assert line['questionText'] == 'What is COVID-19 ?'
        assert line['answerText'] == 'Coronaviruses are a large family of viruses .'


def main():
    test_init()
    test_addExample()
    test_schema_v01()
    test_schema_v02()

if __name__ == '__main__':
    main()
