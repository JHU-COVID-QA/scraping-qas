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
                extra = content.find_all('p')
                for e_ in extra:
                    text_ = e_.get_text()
                    if 'Additional Resources:' in text_:
                        extradata_ = e_.find_next_sibling('ul')
                        soup_ex = MyBeautifulSoup(str(extradata_), 'lxml')
                        extradata_ = soup_ex.get_text()
                        extra_data['referenceURL'] = extradata_
                        # print("extra_data=======", extradata_)

                for i, line in enumerate(body_inside, start=1):
                    soup = MyBeautifulSoup(str(line), 'lxml')
                    contents_ = soup.get_text()

                    # print(i) # check the QA paire count

                    if contents_.find('Q:') != -1:
                        question = soup.find('strong').get_text()
                    else:
                        if contents_.find('Q.') != -1:
                            # found!
                            question_ = soup.find('strong')
                            soup_q = MyBeautifulSoup(str(question_), 'lxml')
                            question = soup_q.get_text().split('Q.')[1]
                            # print("TEST===2", question)

                    if contents_.find('A:') != -1:
                        # found!
                        answer = contents_.split('A:')[1]
                    if contents_.find('A.') != -1:
                        # found!
                        answer = contents_.split('A.')[1]

                    else:
                        # if soup.find_all('ul') != None: #bullet point and 'A
                        #     print("######", soup.find_next_sibling('li'))
                        #     pass

                        pair = soup.find_all('p')
                        # print(pair)
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
                        else: # <p> is one
                            # answer = pair.find_next_sibling('ul')
                            # print("POINT###########", soup.ul)
                            if soup.ul is not None :
                                answer_ = soup.ul
                                soup_ul = MyBeautifulSoup(str(answer_), 'lxml')
                                answer = soup_ul.get_text()

                    # print("question=======", question)
                    # print("answer=======", answer)
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
