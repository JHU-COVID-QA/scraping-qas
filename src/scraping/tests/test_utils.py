from covid_scraping import utils
import subprocess
import json
import unittest
import time

class TestUtils(unittest.TestCase):

    def test_remove_duplicates(self):
        data = []
        for line in open('./schema_v0.2/test_merge_v0.2.jsonl'):
            data.append(json.loads(line))
         
        new_data = utils._remove_duplicates(data)
        self.assertEqual(type(new_data), type(data))
        self.assertLess(len(new_data), len(data))

        self.assertGreater(len(data), len(set([example['ID'] for example in new_data])))


if __name__ == '__main__':
    unittest.main()
