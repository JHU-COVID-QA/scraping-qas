# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
WHO crawler
Expected page to crawl is 
https://www.who.int/news-room/q-a-detail/q-a-coronaviruses
"""
__author__ = "linxy97"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["linxy97", "Adam Poliak"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import datetime, time
import pprint
from urllib import request, response, error, parse
from urllib.request import urlopen
from bs4 import BeautifulSoup, NavigableString, CData, Tag
import jsonlines
import re
import pandas as pd
import uuid

from covid_scraping import test_jsonlines

# from covid_scraping import test_jsonlines


'''
<div class="sf-accordion__panel is-active">
    <div class="sf-accordion__trigger-panel">
        <a href="#" class="sf-accordion__link">
            What is a coronavirus?
        </a>
    </div>
    <div class="sf-accordion__content" style="display: block; opacity: 1;">
        <p class="sf-accordion__summary">
            </p><p>Coronaviruses are a large family of viruses which may cause illness in animals or humans. &nbsp;In humans, several coronaviruses are known to cause respiratory infections ranging from the common cold to more severe diseases such as Middle East Respiratory Syndrome (MERS) and Severe Acute Respiratory Syndrome (SARS). The most recently discovered coronavirus causes coronavirus disease COVID-19.</p>
        <p></p>
    </div>
</div>
'''

name = 'WHO'
url = 'https://www.who.int/news-room/q-a-detail/q-a-coronaviruses'
html = urlopen(url)
soup = BeautifulSoup(html, "lxml")

topics = soup.find_all('', class_='sf-accordion__link')
contents = soup.find_all('div', class_='sf-accordion__content')

link_info = []

timestamp = int(time.time())
# <span>9 March 2020 | Q&amp;A </span>
sourcedate = re.search(r'\d+\s\D*\S\d+', soup.find('', class_='col-sm-7 col-md-7').text).group()
sourcedate = sourcedate.split()
year = sourcedate[2]
day = sourcedate[0]
month = sourcedate[1]
sourcedate = datetime.datetime.strptime(" ".join([day, month[:3], year]), '%d %b %Y').timestamp()

class MyBeautifulSoup(BeautifulSoup):
    '''
    input:
    """
   ...: <td>
   ...:     <font><span>Hello</span><span>World</span></font><br>
   ...:     <span>Foo Bar <span>Baz</span></span><br>
   ...:     <span>Example Link: <a href="https://google.com" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #395c99;font-weight: normal;tex
   ...: t-decoration: underline;">Google</a></span>
   ...: </td>
   ...: """
   output:
      HelloWorld
      Foo Bar Baz
      Example Link: <a href="https://google.com" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #395c99;font-weight: normal;text-decoration: underline;" target="_blank">Google</a>
    '''
    def _all_strings(self, strip=False, types=(NavigableString, CData)):
        for descendant in self.descendants:
            # return "a" string representation if we encounter it
            if isinstance(descendant, Tag) and descendant.name == 'a':
                yield str(descendant)
                # yield str('<"{}">'.format(descendant.get('href', '')))

            # if isinstance(descendant, Tag) and descendant.name == 'a' and descendant.name == 'span':
            #     descendant = descendant.replaceWith('')
            #     yield str(descendant)

            # skip an inner text node inside "a"
            if isinstance(descendant, NavigableString) and descendant.parent.name == 'a':
                continue

            # default behavior
            if (
                (types is None and not isinstance(descendant, NavigableString))
                or
                (types is not None and type(descendant) not in types)):
                continue

            if strip:
                descendant = descendant.strip()
                if len(descendant) == 0:
                    continue
            yield descendant

def topic_to_url(topics, contents):
    for i, topic in enumerate(topics):
        topic_name = topic.get_text().strip()
        content = contents[i].get_text().strip()
        link_info.append({
            'sourceUrl': url,
            'topic': '',
            'content': content, 
            'sourceName': name,
            "dateScraped": time.time(),
            "sourceDate": sourcedate,
            "lastUpdateTime": sourcedate,
            "needUpdate": False,
            "containsURLs": False, #need to make this programmitic
            "typeOfInfo": "QA",
            "isAnnotated": False,
            "responseAuthority": "",
            "questionUUID": str(uuid.uuid1()),
            "answerUUID": str(uuid.uuid1()),
            "exampleUUID": str(uuid.uuid1()),
            "questionText": topic_name,
            "answerText": content,
            "hasAnswer": True,
            "targetEducationLevel": "NA",
            "extraData": {},
        })

def main(info_list):
    topic_to_url(topics, contents)
    output_path = "WHO_v0.1.jsonl"
    with jsonlines.open(output_path, 'w') as writer:
            writer.write_all(info_list)

    test_jsonlines(output_path)
    
if __name__ == "__main__":
    main(link_info)
