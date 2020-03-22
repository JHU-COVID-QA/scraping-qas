import datetime, time
import json
import pprint
import uuid
from urllib.request import urlopen
from bs4 import BeautifulSoup, NavigableString, CData, Tag
import jsonlines

'''
    This scripts are for the CDC "https://www.cdc.gov/coronavirus/2019-ncov/faq.html" site
'''
class Schema():
    def __init__(self, topic, sourcedate, contain_url,
                 response_auth, question, answer, extradata):

        self.timestamp_ = int(time.time())
        self.sourcedate_ = sourcedate
        self.contain_url_ = contain_url
        self.response_auth_ = response_auth
        self.question_ = question
        self.answer_ = answer
        self.extradata_ = extradata

        topic['sourceName'] = 'CDC'
        topic['typeOfInfo'] = 'QA'
        topic['dateScraped'] = float(self.timestamp_)
        topic['sourceDate'] = self.sourcedate_
        topic['lastUpdateTime'] = self.sourcedate_
        topic['needUpdate'] = True
        topic['containsURLs'] = contain_url
        topic['isAnnotated'] = False
        topic['responseAuthority'] = self.response_auth_  # str (if it is at JHU to know who the answer came from)
        topic['questionUUID'] = str(uuid.uuid1())
        topic['answerUUID'] = str(uuid.uuid1())
        topic['exampleUUID'] = str(uuid.uuid1())
        topic['questionText'] = self.question_
        topic['answerText'] = self.answer_
        topic['hasAnswer'] = True
        topic['targetEducationLevel'] = 'NA'
        topic['extraData'] = self.extradata_

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

    def _all_strings(self, strip=False, types=(NavigableString, CData), resource=False):
        for descendant in self.descendants:
            # return "a" string representation if we encounter it
            if isinstance(descendant, Tag) and descendant.name == 'a':
                # print(descendant)
                # < a class ="tp-link-policy" data-domain-ext="gov" href="https://www.usembassy.gov/" >
                # US embassy < span class ="sr-only" > external icon < / span > < span aria-hidden="true" class ="fi cdc-icon-external x16 fill-external" > < / span > < / a >
                # print(descendant.contents) # check the contents inside <a> tag
                # ex: ['best practice', <span class="sr-only">external icon</span>, <span aria-hidden="true" class="fi cdc-icon-external x16 fill-external"></span>]

                if len(descendant.contents) > 0 :
                    for tag in descendant.find_all('span'):
                        # print(tag)
                        tag.replaceWith('')

                ''' to the absolute path url'''
                script = descendant.get('href')
                if str(script).find('https') != -1 or str(script).find('http') != -1 or str(script).find('mailto:') != -1:
                    pass
                else:
                    if descendant.has_attr("href") == True:
                        descendant['href'] = "https://www.cdc.gov" + str(descendant['href'])
                        # print(descendant)

                if resource == False:
                    # print(descendant)
                    yield str(descendant)
                else:
                    # This is for the future 'extraData'
                    yield str('<{}>'.format(descendant.get('href', '')))

            # skip an inner text node inside "a"
            if isinstance(descendant, NavigableString) and descendant.parent.name == 'a':
                # print(descendant)
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

class Crawler():
    def __init__(self):
        # def target_body(self, target_tag: str, target_attr: str, target_attr_string: str)
        url = 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html'
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")

        left_topics = self.target_body('ul', 'class', 'col-md-6 float-left list-group list-group-flush')
        right_topics = self.target_body('ul', 'class', 'col-md-6 float-right list-group list-group-flush')

        # print(left_topics)
        # [<ul class="col-md-6 float-left list-group list-group-flush">
        # <li class="list-group-item"><a href="#basics">Coronavirus Disease 2019 Basics</a></li>
        # <li class="list-group-item"><a href="#spreads">How It Spreads</a></li>

        # <span id="last-reviewed-date">March 19, 2020</span>



        respons_auth = soup.find('div', class_='d-none d-lg-block content-source')
        soup_ = MyBeautifulSoup(str(respons_auth), 'lxml')
        respons_auth = soup_.get_text()

        self.sourcedate = self.date_cal(soup)
        self.link_info = []
        self.left_topics = left_topics
        self.right_topics = right_topics
        self.response_auth = respons_auth

    def date_cal(self, soup):
        date_dict = {'january': '1', 'february': '2', 'march': '3', 'april': '4', 'may': '5', 'june': '6',
                     'july': '7', 'august': '8', 'september': '9', 'october': '10', 'november': '11', 'december': '12'}
        sourcedate = soup.find('span', id='last-reviewed-date').get_text()
        month = sourcedate.split()[0].lower()
        if str(month) in date_dict:
            month = date_dict[month]
        else:
            print("==========Check the update date")
        day = sourcedate.split()[1].split(',')[0]
        year = sourcedate.split()[2]
        sourcedate = datetime.datetime(int(year), int(month), int(day), 0, 0).timestamp()

        return sourcedate

    def target_body(self, target_tag: str, target_attr: str, target_attr_string: str):
        url = 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html'
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")
        # left_topics = soup.find_all('ul', class_='col-md-6 float-left list-group list-group-flush')
        # right_topics = soup.find_all('ul', class_='col-md-6 float-right list-group list-group-flush')
        # attrs = {'aria-labelledby': id_index + '-card-' + str(init)}
        topics = soup.find_all(target_tag, attrs = {target_attr: target_attr_string})

        return topics

    def topic_to_url(self, topic_lists):
        for i, topic in enumerate(topic_lists):
            topic_name = topic.get_text()
            # print(topic_name) # Coronavirus Disease 2019 Basics

            topic_lists_link = topic.get('href')
            # print(topic_lists_link) # #basics

            if str(topic_lists_link).find('#') != -1:
                topic_url = 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html' + topic_lists_link
            else:
                topic_url = 'https://www.cdc.gov' + topic_lists_link
                # print(topic_url)

            self.link_info.append({'topic': topic_name, 'sourceUrl': topic_url})


    def topic_integrate(self, topic_):
        '''
         [{'topic': 'Coronavirus Disease 2019 Basics',
           'sourceUrl': 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html#basics'},
          {'topic': 'How It Spreads', 'sourceUrl: 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html#spreads'},
          {'topic': 'How to Protect Yourself',
           'sourceUrl': 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html#protect'},
          {'topic': 'Symptoms & Testing', 'sourceUrl': 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html#symptoms'}]
        '''
        for child in topic_:
            topic_lists = child.find_all('a', href=True)
            self.topic_to_url(topic_lists)

        return self.link_info

    def sub_topic_QA(self, info_list):
        '''
        Question :
        <div id="accordion-9" class="accordion indicator-plus accordion-white mb-3" role="tablist">
        <div id="accordion-10" class="accordion indicator-plus accordion-white mb-3" role="tablist">
        Answer :
        <div aria-labelledby="accordion-12-card-1" class="collapse show" collapsed="" id="accordion-12-collapse-1" role="tabpanel" style="">
        <div class="card-body"><p>A novel coronavirus is a new coronavirus that has not been previously identified. The virus causing coronavirus disease 2019 (COVID-19), is not the same as the <a href="/coronavirus/types.html">coronaviruses that commonly circulate among humans</a>&nbsp;and cause mild illness, like the common cold.</p>
        <p>A diagnosis with coronavirus 229E, NL63, OC43, or HKU1 is not the same as a COVID-19 diagnosis. Patients with COVID-19 will be evaluated and cared for differently than patients with common coronavirus diagnosis.</p>
        </div>
        </div>
        '''
        try:
            with open('./data/CDC_v0.1.jsonl', 'w') as writer:
                for i, topic in enumerate(info_list, start=len(info_list)+1):
                    extradata = {}
                    # print(i)
                    # print(sub_topic) # {'sourceName': 'Coronavirus Disease 2019 Basics', 'sourceUrl': 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html#basics'}
                    url = topic['sourceUrl']
                    html = urlopen(url)
                    soup = BeautifulSoup(html, "lxml")

                    id_index = 'accordion-' + str(i)
                    subtopic_body = soup.find_all('div', id=id_index)

                    for init, sub_topic in enumerate(subtopic_body, start=1):
                        # print(sub_topic)
                        questions = sub_topic.find_all('div', class_='card-header')
                        # print(questions)

                        # answers = sub_topic.find_all('div', attrs={'aria-labelledby':id_index + '-card-' + str(init)})
                        answers = sub_topic.find_all('div', class_='card-body')

                        # print(answers)
                        for k, (question, answer) in enumerate(zip(questions, answers), start=1):
                            # print(answer)
                            # print(question)
                            soup = MyBeautifulSoup(str(answer), 'lxml')
                            a= soup.get_text()
                            q = question.get_text()
                            # print("========question:", q)
                            # print("========answer:", a)

                            if a.find('http') != -1 or a.find('https') != -1:
                                contain_url = True
                            else:
                                contain_url = False

                            # print(q) # What is a novel coronavirus?
                            # info_list.append({'sub_topic_'+str(k):{'question':q, 'answer':a}})

                            if topic['topic'] == 'Healthcare Professionals and Health Departments':
                                extradata['referenceURL'] = 'https://www.cdc.gov/coronavirus/2019-ncov/hcp/faq.html'
                            else:
                                extradata = {}

                            Schema(topic, self.sourcedate, contain_url, self.response_auth, q, a, extradata)

                            # print(topic)
                            json.dump(topic, writer)
                            writer.write('\n')

                # pp = pprint.PrettyPrinter(indent=4)
                # pp.pprint(info_list[-9:])

        except KeyError:
            pass

    def other_QA(self):
        ''' Need to modify '''
        topics_ = self.target_body('div', 'class', 'card-body bg-quaternary')
        info_list_ = self.topic_integrate(topics_)
        # print(info_list_)

        try:
            for i, topic in enumerate(info_list_, start=1):
                extradata = {}
                # print(sub_topic) # {'sourceName': 'Coronavirus Disease 2019 Basics', 'sourceUrl': 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html#basics'}
                # print(topic)
                url = topic['sourceUrl']
                html = urlopen(url)
                soup = BeautifulSoup(html, "lxml")

                topic_count = len(soup.find_all('h2'))
                # print(topic_count)
                i = i + topic_count
                topic['topic'] = topic['topic'] + '::' + soup.h2.find_next('a')['title']
                # print(topic)

                id_index = 'accordion-' + str(i)
                subtopic_body = soup.find_all('div', id=id_index)

                # print(i)
                # print(subtopic_body)
                for init, sub_topic in enumerate(subtopic_body, start=1):

                    questions = sub_topic.find_all('div', class_='card-header')
                    # print(questions)

                    answers = sub_topic.find_all('div', class_='card-body')
                    # print(answers)

                    for k, (question, answer) in enumerate(zip(questions, answers), start=1):
                        # print(answer)
                        # print(question)
                        soup = MyBeautifulSoup(str(answer), 'lxml')
                        a = soup.get_text()
                        q = question.get_text()

                        if a.find('http') != -1 or a.find('https') != -1:
                            contain_url = True
                        else:
                            contain_url = False

                        if topic['topic'] == 'Healthcare Professionals and Health Departments':
                            extradata['referenceURL'] = 'https://www.cdc.gov/coronavirus/2019-ncov/hcp/faq.html'
                        else:
                            extradata = {}

                        Schema(topic, self.sourcedate, contain_url, self.response_auth, q, a, extradata)

            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(info_list_[-3:])

            # with jsonlines.open('./data/CDC_v0.1-1.jsonl', 'w') as writer:
            #     writer.write_all(self.link_info)

        except KeyError:
            pass



if __name__== '__main__':
    ''' sub_topicQA: cdc main page crawler 
    
    '''
    crw = Crawler()

    crw.topic_integrate(crw.left_topics)
    crw.topic_integrate(crw.right_topics)
    crw.sub_topic_QA(crw.link_info)

    # crw.other_QA()

    # print(crw.link_info)
