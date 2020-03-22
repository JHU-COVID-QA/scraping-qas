import datetime, time
import pprint
from urllib import request, response, error, parse
from urllib.request import urlopen
from bs4 import BeautifulSoup, NavigableString, CData, Tag
import jsonlines
import re
import pandas as pd
import uuid
import jsonlines
import time

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
            "lastUpdateTime": '',
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
    with jsonlines.open('./data/scraping/WHO_v0.1.jsonl', 'w') as writer:
            writer.write_all(info_list)
    
if __name__ == "__main__":
    main(link_info)