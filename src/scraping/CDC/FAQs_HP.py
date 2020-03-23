import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from crawler import Schema, MyBeautifulSoup, Crawler


class General_page():
    ''' This scripts for the 'FAQs for Healthcare Professionals' page
    'https://www.cdc.gov/coronavirus/2019-ncov/hcp/faq.html' '''

    def __init__(self):
        url = 'https://www.cdc.gov/coronavirus/2019-ncov/hcp/faq.html'
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")

        crw = Crawler()

        self.crw = crw
        self.url = url
        self.soup = soup

    def main(self):
        data = {}
        extra_data = {}

        topic_name = self.soup.find('h1', id='content').get_text()
        response_auth = self.soup.find('div', class_='d-none d-lg-block content-source')
        soup_ = MyBeautifulSoup(str(response_auth), 'lxml')
        response_auth = soup_.get_text()
        sourcedate = self.crw.date_cal(self.soup)

        body = self.crw.target_body(self.url, 'div', 'class', 'col-md-12')
        # print(topic_name)

        with open('./data/CDC_FAQs_HP_v0.1.jsonl', 'w') as writer:
            for content in body:
                body_inside = content.find_all('div', class_='mb-5')

                if len(content.find_all('h3')) > 0:
                    topic_name = topic_name + "::" + self.soup.h3.text
                    # print(topic_name)

                '''for extradata'''
                addt = content.find_all('ul')
                for each in addt:
                    soup = MyBeautifulSoup(str(each), 'lxml')
                    extradata_ = soup.get_text()
                    extra_data['referenceURL'] = extradata_
                    # print(extradata)

                for i, line in enumerate(body_inside, start=1):
                    soup = MyBeautifulSoup(str(line), 'lxml')
                    contents = soup.get_text()

                    # print(i) # check the QA paire count

                    if contents.find('Q:') != -1:
                        question = contents.split('Q:')[1]
                    else:
                        question = soup.find('strong').get_text()
                        pass

                    if contents.find('A:') != -1:
                        answer = contents.split('A:')[1]
                    else:
                        pair = soup.find_all('p')
                        # print(len(pair))
                        # print(pair)
                        if len(pair) == 2: # in case of 'A:' no-notation
                            res = [ele for ele in pair]
                            answer = res[-1]
                            soup = MyBeautifulSoup(str(answer), 'lxml')
                            answer = soup.get_text()
                        elif len(pair) > 2: # in case of 'A:' no-notation and lots <p> tag
                            res = [ele for ele in pair]
                            # answer = res[1:-1]
                            answer = ''.join(str(e) for e in res[1:])
                            soup = MyBeautifulSoup(str(answer), 'lxml')
                            answer = soup.get_text()
                        # print("A====", answer)

                    contain_url = self.crw.contain_URL(answer)

                    data['topic'] = topic_name
                    data['sourceUrl'] = self.url
                    Schema(data, sourcedate, contain_url, response_auth,
                           question, answer, extra_data)

                    # print(data)
                    json.dump(data, writer)
                    writer.write('\n')
            print("Data saved!!-- FAQs_HP")






if __name__== '__main__':
    ge_crawler = General_page()
    ge_crawler.main()
