# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
Internal COVID QAs crawler
Expected page to crawl is
COVID19infosheet - Info.tsv
"""
__author__ = "Adam Poliak"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Adam Poliak"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import pandas as pd
import uuid
import jsonlines
import time

from covid_scraping import test_jsonlines


def to_schema(row):
    # ['Question', 'Answer', 'Need to update (Y/N)', 'Tags', 'Author']
    # Question  Answer  Need to update (Y/N)  Tags  Source  Annotator/Author
    data = {
        "sourceUrl": "Internal COVID19infosheet",
        "sourceName": "JHU Public Health" if pd.isna(row['Source']) else "JHU Public Health " + row['Source'],
        "dateScraped": time.time(),
        "sourceDate": float(1584717464),
        "lastUpdateTime": float(1584717464),
        "needUpdate": not(pd.isna(row['Need to update (Y/N)']) and pd.isna(row['Need to update on Turkle (Y/N)'])),
        "containsURLs": True,  # need to make this programmitic
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
        "extraData": {
            "author": "" if pd.isna(row['Annotator/Author']) else row['Annotator/Author']
        }
    }
    return data


def clean_headers(df):
    df = df[df['Question'].map(lambda x: not pd.isna(x))]
    df = df[df['Question'] != 'Questions from Smisha']
    df = df[df['Question'].map(lambda x: not x.startswith("COVID"))]
    df = df[df['Question'].map(
        lambda x: not x.startswith("General Questions"))]
    return df


def main():
    df = pd.read_csv("COVID19infosheet - Info.tsv", sep="\t")

    df = clean_headers(df)
    df['json'] = df.apply(to_schema, axis=1)
    with jsonlines.open('../../../data/scraping/schema_v0.1/interalCOVIDinfosheet_v0.1.jsonl', 'w') as writer:
        writer.write_all(df['json'])

    test_jsonlines(
        '../../../data/scraping/schema_v0.1/interalCOVIDinfosheet_v0.1.jsonl')


if __name__ == '__main__':
    main()
