# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.

__author__ = "Adam Poliak"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Adam Poliak"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

from canada_public_health_scraper import CanadaPublicHealthScraper
from jhu_bloomberg import JHUBloombergScraper
from jhu_hub import JHUHubScraper
from nfid_scraper import NFIDScraper
from whomyth_scraper import WhoMythScraper
from texasHumanResources_scraper import TexasHumanResourceScraper
from clevelandClinic_scraper import ClevelandClinicScraper
from fda_scraper import FDAScraper
from nyt_scraper import NewYorkTimesScraper
from whomyth_scraper import WhoMythScraper
from deepsetAI_scraper import DeepsetAIMasterScraper
from floridaGov_scraper import FloridaGovScraper
from cnn_scraper import CNNScraper
from avma_scraper import AVMAScraper
from jhu_med import JHUMedicineScraper
from vermont_gov import VermontGovScraper
from kansas_gov import KansasGovScraper
from north_dakota import NorthDakotaGovScraper
from delaware_gov import DelawareGovScraper
from oregon_gov import OregonGovScraper
from north_carolina_gov import NorthCarolinaGovScraper
from hawaii_gov import HawaiiGovScraper


def main():
    path = '../../../data/scraping/'

    scrapers = [
                CanadaPublicHealthScraper(path=path, filename='CanadaPublicHealth'),
                JHUBloombergScraper(path=path, filename="JHU-bloomberg"),
                JHUHubScraper(path=path, filename="JHU_hub"),
                NFIDScraper(path=path, filename="NFID"),
                TexasHumanResourceScraper(path=path, filename="TexasHR"),
                ClevelandClinicScraper(path=path, filename="ClevelandClinic"),
                FDAScraper(path=path, filename="FDA"),
                NewYorkTimesScraper(path=path, filename="NYT"),
                WhoMythScraper(path=path, filename="WhoMyth"),
                FloridaGovScraper(path=path, filename='Florida'),
                CNNScraper(path=path, filename='CNN'),
                AVMAScraper(path=path, filename='AVMA'),
                JHUMedicineScraper(path=path, filename="JHU_Medicine"),
                VermontGovScraper(path=path, filename='Vermont'),
                KansasGovScraper(path=path, filename='Kansas'),
                NorthDakotaGovScraper(path=path, filename='North_Dakota'),
                DelawareGovScraper(path=path, filename="Delaware"),
                OregonGovScraper(path=path, filename='Oregon'),
                NorthCarolinaGovScraper(path=path, filename='NorthCarolina'),
                HawaiiGovScraper(path=path, filename='Hawaii')
                ]
    success = []
    for scraper in scrapers:
        try:
            success.append(scraper.scrape())
        except:
            success.append(False)

    success_to_string = lambda x: "Success" if x else "Failure"
    for success, scraper in zip(success, scrapers):
        print(success_to_string(success) + " " + str(scraper.__class__.__name__))

if __name__ == '__main__':
    main()
