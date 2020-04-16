# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
Internal COVID QAs crawler
Expected page to crawl is
COVID19infosheet - Info.tsv
"""
__author__ = "Adam Poliak", "Darius Irani"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Adam Poliak"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import pandas as pd

from covid_scraping import Conversion, Scraper


class InternalQAScraper(Scraper):

    def _prepare_data(self, row):
        if not (self._validate(row.Question) or self._validate(row.Answer)):
            return None
        data = {
            'sourceUrl': "Internal COVID19infosheet",
            'sourceName': "JHU Public Health" if pd.isna(row['Source']) else "JHU Public Health " + row['Source'],
            "sourceDate": float(1584717464),
            "lastUpdateTime": float(1584717464),
            "needUpdate": not pd.isna(row['Need to update (Y/N)']),
            "typeOfInfo": "QA",
            "isAnnotated": True,
            "responseAuthority": "Shivani Pandya or Smisha Agrawal",
            "question": row['Question'],
            "answer": row['Answer'] if not pd.isna(row['Answer']) else "",
            "hasAnswer": not pd.isna(row['Answer']),
            "targetEducationLevel": "NA",
            "topic": [row['Tags']] if not pd.isna(row['Tags']) else [],
            "extraData": {"author": "" if pd.isna(row['Annotator/Author']) else row['Annotator/Author']},
            "targetLocation": "",
            "language": 'en',
        }
        return data

    def _clean_headers(self, df):
        df = df[df['Question'].map(lambda x: not pd.isna(x))]
        df = df[df['Question'] != 'Questions from Smisha']
        df = df[df['Question'].map(lambda x: not x.startswith("COVID"))]
        df = df[df['Question'].map(
            lambda x: not x.startswith("General Questions"))]
        return df

    def _validate(self, field):
        return len(field.strip()) > 0

    def scrape(self):
        converter = Conversion(self._filename, self._path)

        df = pd.read_csv(open("COVID19infosheet - Info.tsv", 'r'), sep="\t")
        df = self._clean_headers(df)
        df['json'] = df.apply(self._prepare_data, axis=1)
        for obj in df['json']:
            if not obj: continue # don't add qa-pair if q or a field is empty
            converter.addExample(obj)            

        converter.write()


def main():
    scraper = InternalQAScraper(path='./', filename='internalCOVIDinfosheet')
    scraper.scrape()


if __name__ == '__main__':
    main()
