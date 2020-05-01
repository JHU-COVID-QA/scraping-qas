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

from internalQAs_scraper import InternalQAScraper
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


def main():
    path = '../../../data/scraping/'

    scraper = InternalQAScraper(
        path=path, filename='internalCOVIDinfosheet')
    scraper.scrape()

    scraper = CanadaPublicHealthScraper(
        path=path, filename='CanadaPublicHealth')
    scraper.scrape()

    scraper = JHUBloombergScraper(path=path, filename="JHU-bloomberg")
    scraper.scrape()

    scraper = JHUHubScraper(path=path, filename="JHU_hub")
    scraper.scrape()

    scraper = NFIDScraper(path=path, filename="NFID")
    scraper.scrape()

    scraper = TexasHumanResourceScraper(path=path, filename="TexasHR")
    scraper.scrape()

    scraper = ClevelandClinicScraper(path=path, filename="ClevelandClinic")
    scraper.scrape()

    scraper = FDAScraper(path=path, filename="FDA")
    scraper.scrape()

    scraper = NewYorkTimesScraper(path=path, filename="NYT")
    scraper.scrape()

    scraper = WhoMythScraper(path=path, filename="WhoMyth")
    scraper.scrape()

    #scraper = DeepsetAIMasterScraper(path=path, filename="DeepsetAI")
    # scraper.scrape()

    scraper = FloridaGovScraper(path=path, filename='Florida')
    scraper.scrape()

    scraper = CNNScraper(path=path, filename='CNN')
    scraper.scrape()

    scraper = AVMAScraper(path=path, filename='AVMA')
    scraper.scrape()

    scraper = JHUMedicineScraper(path=path, filename="JHU_Medicine")
    scraper.scrape()

    scraper = VermontGovScraper(path=path, filename='Vermont')
    scraper.scrape()


if __name__ == '__main__':
    main()
