# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
Merging Script for Gold and Staged Rescrape Data
"""
__author__ = "Milind Agarwal"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Milind Agarwal"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import jsonlines
from fuzzywuzzy import fuzz
import os
import time

fuzz_threshold_ques = 60
fuzz_threshold_ans = 60

for file in os.listdir("../../../data/scraping/schema_v0.1/stage"):
    if file.endswith(".jsonl"):
        split = file.split('_STAGE')
        goldName = "../../../data/scraping/schema_v0.1/" + split[0] + split[1]
        stageName = "../../../data/scraping/schema_v0.1/stage/" + file

        goldData = []
        goldQues = []
        with jsonlines.open(goldName) as q:
            for line in q.iter():
                goldData.append(line)
                goldQues.append(line['questionText'])

        with jsonlines.open(stageName) as f:
            print('\n\n FILE 1: ' + stageName + '\n')
            cur = f.iter()
            for line in cur:
                ques = line['questionText']
                ans = line['answerText']
                fuzzy_PR_ques = lambda x: fuzz.partial_ratio(ques,x)
                goldQuesScores = list(map(fuzzy_PR_ques, goldQues))
                found = (sum(i >= fuzz_threshold_ques for i in goldQuesScores) > 0)
                if not found:
                    print('Not found. Adding this json object to the gold data')
                    goldData.append(line)

                else:
                    maxix = goldQuesScores.index(max(goldQuesScores))
                    goldA = goldData[maxix]['answerText']
                    ansScore = fuzz.partial_ratio(ans, goldA)

                    # check if the new answer matches the existing answer for that question:
                    if ansScore > fuzz_threshold_ans:
                        print('Answer match found. Updating metadata')
                        goldData[maxix]['dateScraped'] = time.time()
                        goldData[maxix]['lastUpdateTime'] = time.time()

                    else:
                        print('Answer match NOT found. Updating answer and metadata.')
                        goldData[maxix]['answerText'] = ans
                        goldData[maxix]['answerUUID'] = line['answerUUID']
                        goldData[maxix]['dateScraped'] = time.time()
                        goldData[maxix]['lastUpdateTime'] = time.time()
                        goldData[maxix]['hasAnswer'] = True


        # Write the new data
        with jsonlines.open(goldName, mode='w') as writer:
            writer.write_all(goldData)
