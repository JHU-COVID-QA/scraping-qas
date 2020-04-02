from covid_scraping import Conversion, test_jsonlines
import subprocess
import jsonlines
import unittest


class TestConversion(unittest.TestCase):

    def test_init(self):
        converter = Conversion('test', '../../../data/scraping')
        assert converter._file_prefix is 'test'
        assert isinstance(converter._examples, list)

    def test_addExample(self):
        converter = Conversion('test', '../../../data/scraping')
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

    def test_schema_v01(self):
        test_jsonlines('../../../data/scraping/schema_v0.1/test_v0.1.jsonl', version='v0.1')
        with jsonlines.open('../../../data/scraping/schema_v0.1/test_v0.1.jsonl', 'r') as reader:
            line = reader.read()
            assert line['questionText'] == 'What is COVID-19 ?'
            assert line['answerText'] == 'Coronaviruses are a large family of viruses .'
        subprocess.call(['rm','../../../data/scraping/schema_v0.1/test_v0.1.jsonl'])

    def test_schema_v02(self):
        test_jsonlines('../../../data/scraping/schema_v0.2/test_v0.2.jsonl', version='v0.2')
        with jsonlines.open('../../../data/scraping/schema_v0.2/test_v0.2.jsonl', 'r') as reader:
            line = reader.read()
            assert line['questionText'] == 'What is COVID-19 ?'
            assert line['answerText'] == 'Coronaviruses are a large family of viruses .'
        subprocess.call(['rm','../../../data/scraping/schema_v0.2/test_v0.2.jsonl'])


if __name__ == '__main__':
    unittest.main()
