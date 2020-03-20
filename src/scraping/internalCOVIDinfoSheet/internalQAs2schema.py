import pandas as pd
import uuid
import jsonlines
import time

def to_schema(row):
  # ['Question', 'Answer', 'Need to update (Y/N)', 'Tags', 'Author']
  data = {
  "sourceUrl": "Internal COVID19infosheet",
  "sourceName": "JHU Public Health",
  "dateScraped": time.time(),
  "sourceDate": float(1584717464),
  "lastUpdateTime": float(1584717464),
  "needUpdate": True,
  "containsURLs": True, #need to make this programmitic
  "typeOfInfo": "QA",
  "isAnnotated": True,
  "responseAuthority": "Shivani Pandya or Smisha Agrawal",
  "questionUUID": str(uuid.uuid1()),
  "answerUUID": str(uuid.uuid1()),
  "exampleUUID": str(uuid.uuid1()),
  "questionText": row['Question'],
  "answerText": row['Answer'] if not pd.isna(row['Answer']) else "",
  "hasAnswer": not pd.isna(row['Answer']),
  "targetEducationLevel": "NA",
  "topic": row['Tags'] if not pd.isna(row['Tags']) else "",
  "extraData": {}}
  return data

def main():
  df = pd.read_csv("COVID19infosheet - Info.tsv", sep="\t")
  df = df[df['Question'].map(lambda x: not pd.isna(x))]
  df['json'] = df.apply(to_schema, axis=1)
  with jsonlines.open('../../../data/scraping/interalCOVIDinfosheet_v0.1.jsonl', 'w') as writer:
    writer.write_all(df['json'])


if __name__ == '__main__':
  main()
