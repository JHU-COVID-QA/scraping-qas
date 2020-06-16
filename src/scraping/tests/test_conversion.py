from covid_scraping import Conversion, test_jsonlines
import subprocess
import jsonlines
import unittest
import time

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

    def test_schema_v03(self):
        test_jsonlines('./schema_v0.3/test_v0.3.jsonl', version='v0.3')
        with jsonlines.open('./schema_v0.3/test_v0.3.jsonl', 'r') as reader:
            line = reader.read()
            self.assertEqual(line['questionText'], 'What is COVID-19?')
            self.assertEqual(
                line['answerText'],
                'Coronaviruses are a large family of viruses.')

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

    def test_blank_question_exception(self):
        with self.assertRaises(ValueError) as e:
            converter = Conversion('test', '.')
            converter.addExample({
                'sourceUrl': 'example.com',
                'sourceName': "example",
                "needUpdate": True,
                "typeOfInfo": "QA",
                "isAnnotated": False,
                "responseAuthority": "",
                "question": '               ',
                "answer": '<a href="example.com/dir1">What is COVID-19?</a>',
                "hasAnswer": True,
                "targetEducationLevel": "NA",
                "topic": ['topic1', 'topic2'],
                "extraData": {'hello': 'goodbye'},
                "targetLocation": "US",
                "language": 'en',
            })

    def test_blank_answer_exception(self):
        with self.assertRaises(ValueError) as e:
            converter = Conversion('test', '.')
            converter.addExample({
                'sourceUrl': 'example.com',
                'sourceName': "example",
                "needUpdate": True,
                "typeOfInfo": "QA",
                "isAnnotated": False,
                "responseAuthority": "",
                "question": '<a href="example.com/dir1">What is COVID-19?</a>',
                "answer": '\n    \n',
                "hasAnswer": True,
                "targetEducationLevel": "NA",
                "topic": ['topic1', 'topic2'],
                "extraData": {'hello': 'goodbye'},
                "targetLocation": "US",
                "language": 'en',
            })

    def test_uuid_preservation_no_change(self):
        subprocess.run(
            ['touch', './schema_v0.3/test_uuid_preservation_v0.3.jsonl'])
        converter = Conversion('test_uuid_preservation', '.')
        converter.addExample({
            'sourceUrl': 'uuid.com',
            'sourceName': "uuid",
            "needUpdate": True,
            "typeOfInfo": "QA",
            "isAnnotated": False,
            "responseAuthority": "",
            "question": 'Hello, this is the example question?',
            "answer": 'Hello this is the example responce',
            "hasAnswer": True,
            "targetEducationLevel": "NA",
            "topic": ['topic1', 'topic2'],
            "extraData": {'hello': 'goodbye'},
            "targetLocation": "US",
            "language": 'en',
        })
        converter.write()
        with jsonlines.open('./schema_v0.3/test_uuid_preservation_v0.3.jsonl') as reader:
            line = reader.read()
            q_uuid = line['questionUUID']
            a_uuid = line['answerUUID']
        converter = Conversion('test_uuid_preservation', '.')
        converter.addExample({
            'sourceUrl': 'uuid.com',
            'sourceName': "uuid",
            "needUpdate": True,
            "typeOfInfo": "QA",
            "isAnnotated": False,
            "responseAuthority": "",
            "question": 'Hello, this is the example question?',
            "answer": 'Hello this is the example responce',
            "hasAnswer": True,
            "targetEducationLevel": "NA",
            "topic": ['topic1', 'topic2'],
            "extraData": {'hello': 'goodbye'},
            "targetLocation": "US",
            "language": 'en',
        })
        converter.write()
        with jsonlines.open('./schema_v0.3/test_uuid_preservation_v0.3.jsonl') as reader:
            line = reader.read()
            new_q_uuid = line['questionUUID']
            new_a_uuid = line['answerUUID']
        self.assertEqual(q_uuid, new_q_uuid)
        self.assertEqual(a_uuid, new_a_uuid)
        subprocess.run(
            ['rm', './schema_v0.3/test_uuid_preservation_v0.3.jsonl'])

    def test_uuid_preservation_new_responce(self):
        subprocess.run(
            ['touch', './schema_v0.3/test_uuid_preservation_v0.3.jsonl'])

        converter = Conversion('test_uuid_preservation', '.')
        converter.addExample({
            'sourceUrl': 'uuid.com',
            'sourceName': "uuid",
            "needUpdate": True,
            "typeOfInfo": "QA",
            "isAnnotated": False,
            "responseAuthority": "",
            "question": 'Hello, this is the example question?',
            "answer": 'Hello this is the example responce',
            "hasAnswer": True,
            "targetEducationLevel": "NA",
            "topic": ['topic1', 'topic2'],
            "extraData": {'hello': 'goodbye'},
            "targetLocation": "US",
            "language": 'en',
        })
        converter.write()
        with jsonlines.open('./schema_v0.3/test_uuid_preservation_v0.3.jsonl') as reader:
            line = reader.read()
            q_uuid = line['questionUUID']
            a_uuid = line['answerUUID']
        converter = Conversion('test_uuid_preservation', '.')
        converter.addExample({
            'sourceUrl': 'uuid.com',
            'sourceName': "uuid",
            "needUpdate": True,
            "typeOfInfo": "QA",
            "isAnnotated": False,
            "responseAuthority": "",
            "question": 'Hello, this is the example question?',
            "answer": 'This completely different this should cause a new UUID',
            "hasAnswer": True,
            "targetEducationLevel": "NA",
            "topic": ['topic1', 'topic2'],
            "extraData": {'hello': 'goodbye'},
            "targetLocation": "US",
            "language": 'en',
        })
        converter.write()
        with jsonlines.open('./schema_v0.3/test_uuid_preservation_v0.3.jsonl') as reader:
            line = reader.read()
            new_q_uuid = line['questionUUID']
            new_a_uuid = line['answerUUID']
        self.assertEqual(q_uuid, new_q_uuid)
        self.assertNotEqual(a_uuid, new_a_uuid)
        subprocess.run(
            ['rm', './schema_v0.3/test_uuid_preservation_v0.3.jsonl'])

    def test_id_preservation_no_change(self):
        subprocess.run(
            ['touch', './schema_v0.3/test_id_preservation_v0.3.jsonl'])
        converter = Conversion('test_id_preservation', '.')
        converter.addExample({
            'sourceUrl': 'uuid.com',
            'sourceName': "uuid",
            "needUpdate": True,
            "typeOfInfo": "QA",
            "isAnnotated": False,
            "responseAuthority": "",
            "question": 'Hello, this is the example question?',
            "answer": 'Hello this is the example responce',
            "hasAnswer": True,
            "targetEducationLevel": "NA",
            "topic": ['topic1', 'topic2'],
            "extraData": {'hello': 'goodbye'},
            "targetLocation": "US",
            "language": 'en',
        })
        converter.write()
        with jsonlines.open('./schema_v0.3/test_id_preservation_v0.3.jsonl') as reader:
            line = reader.read()
            id = line['ID']
        converter = Conversion('test_id_preservation', '.')
        converter.addExample({
            'sourceUrl': 'uuid.com',
            'sourceName': "uuid",
            "needUpdate": True,
            "typeOfInfo": "QA",
            "isAnnotated": False,
            "responseAuthority": "",
            "question": 'Hello, this is the example question?',
            "answer": 'Hello this is the example responce',
            "hasAnswer": True,
            "targetEducationLevel": "NA",
            "topic": ['topic1', 'topic2'],
            "extraData": {'hello': 'goodbye'},
            "targetLocation": "US",
            "language": 'en',
        })
        converter.write()
        with jsonlines.open('./schema_v0.3/test_id_preservation_v0.3.jsonl') as reader:
            line = reader.read()
            new_id = line['ID']
        self.assertEqual(id, new_id)
        subprocess.run(
            ['rm', './schema_v0.3/test_id_preservation_v0.3.jsonl'])

    def test_id_preservation_fuzzy_change(self):
        subprocess.run(
            ['touch', './schema_v0.3/test_id_preservation_v0.3.jsonl'])
        converter = Conversion('test_id_preservation', '.')
        converter.addExample({
            'sourceUrl': 'uuid.com',
            'sourceName': "uuid",
            "needUpdate": True,
            "typeOfInfo": "QA",
            "isAnnotated": False,
            "responseAuthority": "",
            "question": 'Hello, this is the example question?',
            "answer": 'Hello this is the example responce',
            "hasAnswer": True,
            "targetEducationLevel": "NA",
            "topic": ['topic1', 'topic2'],
            "extraData": {'hello': 'goodbye'},
            "targetLocation": "US",
            "language": 'en',
        })
        converter.write()
        with jsonlines.open('./schema_v0.3/test_id_preservation_v0.3.jsonl') as reader:
            line = reader.read()
            id = line['ID']
        converter = Conversion('test_id_preservation', '.')
        converter.addExample({
            'sourceUrl': 'uuid.com',
            'sourceName': "uuid",
            "needUpdate": True,
            "typeOfInfo": "QA",
            "isAnnotated": False,
            "responseAuthority": "",
            "question": 'Hello, but this is the example question?',
            "answer": 'Hello this is the example responce',
            "hasAnswer": True,
            "targetEducationLevel": "NA",
            "topic": ['topic1', 'topic2'],
            "extraData": {'hello': 'goodbye'},
            "targetLocation": "US",
            "language": 'en',
        })
        converter.write()
        with jsonlines.open('./schema_v0.3/test_id_preservation_v0.3.jsonl') as reader:
            line = reader.read()
            new_id = line['ID']
        self.assertEqual(id, new_id)
        subprocess.run(
            ['rm', './schema_v0.3/test_id_preservation_v0.3.jsonl'])

    def test_time_consistency(self):
        subprocess.run(
            ['touch', './schema_v0.3/test_time_consistency_v0.3.jsonl'])
        converter = Conversion('test_time_consistency', '.')
        converter.addExample({
            'sourceUrl': 'time.com',
            'sourceName': "time",
            "needUpdate": True,
            "typeOfInfo": "QA",
            "isAnnotated": False,
            "responseAuthority": "",
            "question": 'Hello, my time should match my next line?',
            "answer": 'Hello this is the example responce',
            "hasAnswer": True,
            "targetEducationLevel": "NA",
            "topic": ['topic1', 'topic2'],
            "extraData": {'hello': 'goodbye'},
            "targetLocation": "US",
            "language": 'en',
        })
        converter.addExample({
            'sourceUrl': 'time.com',
            'sourceName': "uuid",
            "needUpdate": True,
            "typeOfInfo": "QA",
            "isAnnotated": False,
            "responseAuthority": "",
            "question": 'Do I match the above line time? Please say yes!',
            "answer": 'Hello this is the example responce',
            "hasAnswer": True,
            "targetEducationLevel": "NA",
            "topic": ['topic1', 'topic2'],
            "extraData": {'hello': 'goodbye'},
            "targetLocation": "US",
            "language": 'en',
        })
        converter.write()
        with jsonlines.open('./schema_v0.3/test_time_consistency_v0.3.jsonl') as reader:
            line = reader.read()
            dateLastChanged_0 = line['dateLastChanged']
            line = reader.read()
            dateLastChanged_1 = line['dateLastChanged']
        self.assertEqual(dateLastChanged_0, dateLastChanged_1)
        subprocess.run(
            ['rm', './schema_v0.3/test_time_consistency_v0.3.jsonl'])

    def test_remove_unseen(self):
        subprocess.run(
            ['touch', './schema_v0.3/test_remove_unseen_v0.3.jsonl'])
        converter = Conversion('test_remove_unseen', '.')
        converter.addExample({
            'sourceUrl': 'time.com',
            'sourceName': "time",
            "needUpdate": True,
            "typeOfInfo": "QA",
            "isAnnotated": False,
            "responseAuthority": "",
            "question": 'Hello, my time should match my next line?',
            "answer": 'Hello this is the example responce',
            "hasAnswer": True,
            "targetEducationLevel": "NA",
            "topic": ['topic1', 'topic2'],
            "extraData": {'hello': 'goodbye'},
            "targetLocation": "US",
            "language": 'en',
        })
        converter.write()
        converter = Conversion('test_remove_unseen', '.')
        converter.addExample({
            'sourceUrl': 'time.com',
            'sourceName': "time",
            "needUpdate": True,
            "typeOfInfo": "QA",
            "isAnnotated": False,
            "responseAuthority": "",
            "question": 'I am completely new?',
            "answer": 'I am unique! I am special! I matter!',
            "hasAnswer": True,
            "targetEducationLevel": "NA",
            "topic": ['topic1', 'topic2'],
            "extraData": {'hello': 'goodbye'},
            "targetLocation": "US",
            "language": 'en',
        })
        converter.write()
        with open('./schema_v0.3/test_remove_unseen_v0.3.jsonl') as reader:
            self.assertEqual(len(reader.readlines()), 1)

if __name__ == '__main__':
    unittest.main()
