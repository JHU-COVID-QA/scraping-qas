from covid_scraping import Conversion, test_jsonlines
import subprocess
import jsonlines
import unittest


class TestConversion(unittest.TestCase):

    def test_init(self):
        converter = Conversion('test', '.')
        self.assertEqual(converter._file_prefix, 'test')
        self.assertEqual(converter._examples, [])

    def test_addExample(self):
        converter = Conversion('test', '.')
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
        self.assertEqual(len(converter._examples), 1)
        self.assertEqual(converter.write(), True)

    def test_schema_v01(self):
        test_jsonlines('./schema_v0.1/test_v0.1.jsonl', version='v0.1')
        with jsonlines.open('./schema_v0.1/test_v0.1.jsonl', 'r') as reader:
            line = reader.read()
            self.assertEqual(line['questionText'], 'What is COVID-19?')
            self.assertEqual(line['answerText'], 'Coronaviruses are a large family of viruses.')

    def test_schema_v02(self):
        test_jsonlines('./schema_v0.2/test_v0.2.jsonl', version='v0.2')
        with jsonlines.open('./schema_v0.2/test_v0.2.jsonl', 'r') as reader:
            line = reader.read()
            self.assertEqual(line['questionText'], 'What is COVID-19?')
            self.assertEqual(line['answerText'], 'Coronaviruses are a large family of viruses.')

    def test_key_exception(self):
        with self.assertRaises(KeyError) as ke:
            converter = Conversion('test', '.')
            converter.addExample({
                'sourceUrl': 'example.com',
                'language': 'en',
            })

    def test_value_exception(self):
        with self.assertRaises(ValueError) as ve:
            converter = Conversion('test', '.')
            converter.addExample({
            'sourceUrl': ['example.com'],
            "language": 'en',
            })


    def test_blank_answer_exception(self):
        with self.assertRaises(Exception) as e:
            converter = Conversion('test', '.')
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
            "answer": '',
            "hasAnswer": True,
            "targetEducationLevel": "NA",
            "topic": ['topic1', 'topic2'],
            "extraData": {'hello': 'goodbye'},
            "targetLocation": "US",
            "language": 'en',
        })



if __name__ == '__main__':
    unittest.main()
