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

import abc


class Scraper(metaclass=abc.ABCMeta):  # abc.ABC):
    """Scraper class that scrapes a website for FAQs and stores the output to a file"""

    def __init__(self, *, path, filename):
        self._path = path
        self._filename = filename

    @abc.abstractmethod
    def scrape(self):
        """Extracts faqs, converts them using the conversion class
        params: None
        returns: boolean indicating success
            return conversion.write()
        """
        pass
