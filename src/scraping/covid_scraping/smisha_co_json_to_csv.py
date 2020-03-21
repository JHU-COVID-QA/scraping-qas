import json
import csv
from datetime import datetime

data = []
with open('../../../data/scraping/interalCOVIDinfosheet_v0.1.jsonl', 'r') as input:
    for line in input:
        data.append(json.loads(line))

output_data = []
output_keys=["question","answer"]
for q in data:
    q_dict = {"question":"","answer":""}
    if  q['hasAnswer']:
        q_dict["question"]=q["questionText"]
        q_dict["answer"]=q["answerText"] + "Source: {}, updated: {}".format(q['sourceName'],datetime.fromtimestamp(q['lastUpdateTime']).strftime("%A, %B %d, %Y %I:%M:%S"))
        output_data.append(q_dict)

with open('../../../data/scraping/interalCOVIDinfosheet_v0.1.csv', 'w') as output:
    writer = csv.DictWriter(output,fieldnames=output_keys)
    writer.writerows(output_data)