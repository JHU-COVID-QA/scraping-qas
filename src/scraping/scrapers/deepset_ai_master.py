# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
COVID-QA crawler
This script runs a series crawlers written by deepset-ai.
Here is link to their work.
https://github.com/deepset-ai/COVID-QA/tree/master/datasources/scrapers
"""
__author__ = "Max Fleming"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Max Fleming"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import logging
import time
import pandas as pd
from scrapy.crawler import CrawlerProcess
from covid_scraping import Scraper, Conversion
from deepset_ai.Arbeitsagentur_scraper import CovidScraper as Arbeitsagentur
from deepset_ai.BAUA_scraper import CovidScraper as BAUA
from deepset_ai.BMAS_scraper import CovidScraper as BMAS
from deepset_ai.BMG_scraper import CovidScraper as BMG
from deepset_ai.BMWI_scraper import CovidScraper as BMWI
from deepset_ai.BVF_scraper import CovidScraper as BVF
from deepset_ai.BZgA_scraper import CovidScraper as BZgA
from deepset_ai.BerlinerSenat_scraper import CovidScraper as BerlinerSenat
from deepset_ai.Bundesregierung_scraper import CovidScraper as Bundesregierung
from deepset_ai.CDC_Children_scraper import CovidScraper as CDC_Children
from deepset_ai.CDC_Individuals_scraper import CovidScraper as CDC_Individuals
from deepset_ai.CDC_Pregnancy_scraper import CovidScraper as CDC_Pregnancy
from deepset_ai.CDC_Travel_scraper import CovidScraper as CDC_Travel
from deepset_ai.CDC_Water_scraper import CovidScraper as CDC_Water
from deepset_ai.ECDC_scraper import CovidScraper as ECDC
from deepset_ai.FHM_EN_scraper import CovidScraper as FHM_EN
from deepset_ai.FHM_SV_scraper import CovidScraper as FHM_SV
from deepset_ai.GOV_pl_scraper import CovidScraper as GOV_pl
from deepset_ai.IHK_scraper import CovidScraper as IHK
from deepset_ai.KBV_scraper import CovidScraper as KVB
from deepset_ai.RKI_scraper import CovidScraper as RKI
from deepset_ai.Salute_IT_scraper import CovidScraper as Salute_IT
from deepset_ai.UNICEF_scraper import CovidScraper as UNICEF
from deepset_ai.WHO_scraper import CovidScraper as WHO

RESULTS = []
class Pipeline(object):
    def process_item(self, item, spider):
        df = pd.DataFrame.from_dict(item)
        RESULTS.append(df)


class DeepsetAIMasterScraper(Scraper):
    def scrape(self):
        scraper_list = [
            Arbeitsagentur,
            BAUA,
            BMAS,
            BMG,
            BMWI,
            BVF,
            BZgA,
            BerlinerSenat,
            Bundesregierung,
            CDC_Children,
            CDC_Individuals,
            CDC_Pregnancy,
            CDC_Travel,
            CDC_Water,
            ECDC,
            FHM_EN,
            FHM_SV,
            GOV_pl,
            IHK,
            KVB,
            RKI,
            Salute_IT,
            UNICEF,
            WHO,
        ]
        logger = logging.getLogger(__name__)
        logging.disable(logging.WARNING)
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'ITEM_PIPELINES': {'__main__.Pipeline': 1}
        })
        for crawler in scraper_list:
            process.crawl(crawler)
        process.start()
        df = pd.concat(RESULTS)
        converter = Conversion(self._filename, self._path)
        for _, row in df.iterrows():
            converter.addExample({
                    'sourceUrl': row.link,
                    'sourceName': row.source,
                    "sourceDate": time.time(),
                    "lastUpdateTime": time.time(),
                    "needUpdate": True,
                    "typeOfInfo": "QA",
                    "isAnnotated": False,
                    "responseAuthority": "",
                    "question": row.question,
                    "answer": row.answer_html,
                    "hasAnswer": bool(row.answer),
                    "targetEducationLevel": "NA",
                    "topic": [],
                    "extraData": {},
                    "targetLocation": row.country,
                    "language": row.lang,
                })
        return converter.write()




def main():
    scraper = DeepsetAIMasterScraper(path='./', filename = 'DeepsetAI')
    scraper.scrape()
if __name__ == "__main__":
    main()
