import datetime, time
import json
import pprint
import uuid
from urllib.request import urlopen
from bs4 import BeautifulSoup, NavigableString, CData, Tag
import jsonlines
import re

'''
<ul class="col-md-6 float-left list-group list-group-flush">
    <li class="list-group-item"><a href="#basics">Coronavirus Disease 2019 Basics</a></li>
    <li class="list-group-item"><a href="#spreads">How It Spreads</a></li><li class="list-group-item"><a href="#protect">How to Protect Yourself</a></li><li class="list-group-item">
    <a href="#symptoms">Symptoms &amp; Testing</a></li>				</ul>


<ul class="col-md-6 float-right list-group list-group-flush">
	<li class="list-group-item"><a href="#hcp">Healthcare Professionals and Health Departments</a></li><li class="list-group-item">
	<a href="#funerals">COVID-19 and Funerals</a></li>
	<li class="list-group-item"><a href="#cdc">What CDC is Doing</a></li><li class="list-group-item"><a href="#animals">COVID-19 and Animals</a></li></ul>
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

        url = 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html'
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")

        left_topics = soup.find_all('ul', class_='col-md-6 float-left list-group list-group-flush')
        right_topics = soup.find_all('ul', class_='col-md-6 float-right list-group list-group-flush')

        # print(left_topics)
        # [<ul class="col-md-6 float-left list-group list-group-flush">
        # <li class="list-group-item"><a href="#basics">Coronavirus Disease 2019 Basics</a></li>
        # <li class="list-group-item"><a href="#spreads">How It Spreads</a></li>

        timestamp = int(time.time())
        # <span id="last-reviewed-date">March 19, 2020</span>
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

        respons_auth = soup.find('div', class_='d-none d-lg-block content-source')
        soup_ = MyBeautifulSoup(str(respons_auth), 'lxml')
        respons_auth = soup_.get_text()

        self.sourcedate = sourcedate
        self.timestamp = timestamp
        self.link_info = []
        self.left_topics = left_topics
        self.right_topics = right_topics
        self.response_auth = respons_auth

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


    def extract_from_accordian(self, topic, i=1):
        extradata = {}
        # print(i)
        # print(sub_topic) # {'sourceName': 'Coronavirus Disease 2019 Basics', 'sourceUrl': 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html#basics'}
        url = topic['sourceUrl']
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")

        id_index = 'accordion-' + str(i)
        subtopic_body = soup.find_all('div', id=id_index)

        contain_url_list = []
        q_list = []
        a_list = []
        extradata_list = []
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
                contain_url_list.append(contain_url)
                q_list.append(q)
                a_list.append(a)
                extradata_list.append(extradata)
        return contain_url_list, q_list, a_list, extradata_list


    def extract_from_page(self, topic, class_name, header_type):
        extradata = {}
        url = topic['sourceUrl']
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")

        subtopic_body = soup.find_all('div', class_=class_name)

        contain_url_list = []
        q_list = []
        a_list = []
        extradata_list = []
        for init, sub_topic in enumerate(subtopic_body):
            questions = sub_topic.find_all(header_type)

            answers = []
            for question in questions:
                next_node = question.nextSibling
                answer = []
                while next_node is not None:
                    if isinstance(next_node, Tag):
                        if next_node.name == header_type:
                            break
                        answer.append(next_node)
                    next_node = next_node.nextSibling
                answers.append(answer)

            for k, (question, answer) in enumerate(zip(questions, answers), start=1):
                soup = MyBeautifulSoup(''.join([str(a) for a in answer]), 'lxml')
                a = soup.get_text()
                q = question.get_text()
                if 'href' in a:
                    link_soup = BeautifulSoup(a, "lxml")
                    for link in link_soup.find_all('a'):
                        extradata[link.text] = link.get('href')
                    contain_url = True
                else:
                    contain_url = False
                contain_url_list.append(contain_url)
                q_list.append(q)
                a_list.append(a)
                extradata_list.append(extradata)
        return contain_url_list, q_list, a_list, extradata_list

    def extract_from_page_bolded_questions(self, topic, class_name, header_type):
        extradata = {}
        url = topic['sourceUrl']
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")

        subtopic_body = soup.find_all('div', class_=class_name)

        contain_url_list = []
        q_list = []
        a_list = []
        extradata_list = []
        for init, sub_topic in enumerate(subtopic_body):
            subtopics = sub_topic.find_all(header_type)

            questions = []
            answers = []
            for subtopic in subtopics:
                next_node = subtopic.nextSibling
                answer = []
                while next_node is not None:
                    if isinstance(next_node, Tag):
                        if next_node.name == header_type:
                            break
                        if next_node.find('strong'):
                            """
                            TODO: Fix issue where question and answer are contained in single <p> tag separated by <br>
                            """
                            questions.append(next_node.text)
                        else:
                            answer.append(next_node)
                    next_node = next_node.nextSibling
                answers.append(answer)

            if sub_topic.find('a') is not None:
                subtopics = [a.get('title') for a in sub_topic.find_all('a') if a.get('title')]

            for k, (question, answer) in enumerate(zip(questions, answers), start=1):
                soup = MyBeautifulSoup(''.join([str(a) for a in answer]), 'lxml')
                a = soup.get_text()
                q = question
                print("========question:", q)
                print("========answer:", a)
                if 'href' in a:
                    link_soup = BeautifulSoup(a, "lxml")
                    for link in link_soup.find_all('a'):
                        extradata[link.text] = link.get('href')
                    contain_url = True
                else:
                    contain_url = False
                contain_url_list.append(contain_url)
                extradata_list.append(extradata)
        return contain_url_list, q_list, a_list, extradata_list


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
                    contain_url_list, q_list, a_list, extradata_list = self.extract_from_accordian(topic, i)
                    for contain_url, q, a, extradata in zip(contain_url_list, q_list, a_list, extradata_list):
                        Schema(topic, self.sourcedate, contain_url, self.response_auth, q, a, extradata)
                        # Schema(topic, self.sourcedate, contain_url, self.response_auth, q, a, '')

                        # print(topic)
                        json.dump(topic, writer)
                        writer.write('\n')

                    # with jsonlines.open('./data/CDC_v0.1.jsonl', 'w') as writer:
                    #     writer.write_all(topic)

            # pp = pprint.PrettyPrinter(indent=4)
            # pp.pprint(info_list[-9:])

        except KeyError:
            pass

    def other_QA(self):
        faq = {'accordian': ['Travel', 'K-12 Schools and Childcare Program Administrators', 'Community events: for administrators and individuals'],
               'h4_header': ['Pregnant Women and COVID-19', 'Water Transmission'],
               'h2_header': ['Healthcare Professionals', 'Laboratory Diagnostic Panels', 'Laboratory Biosafety', 'Personal Protective Equipment'],
               'h3_header': ['Healthcare Infection']}
        topics_ = self.target_body('div', 'class', 'card-body bg-quaternary')
        titles_ = [topic for topic in [topic.text for topic in topics_][0].split('\n') if topic] # dropdown information extracted elsewhere?
        info_list_ = self.topic_integrate(topics_)
        info_list_ = [info for info in info_list_ if info['topic'] in titles_]
        try:
            for title, topic in zip(titles_, info_list_):
                if title in faq['accordian']:
                    """ TODO: figure out how to automate detection """
                    contain_url_list, q_list, a_list, extradata_list = self.extract_from_accordian(topic)
                elif title in faq['h4_header']:
                    contain_url_list, q_list, a_list, extradata_list = self.extract_from_page(topic, 'card-body', 'h4')
                elif title in faq['h3_header']:
                    contain_url_list, q_list, a_list, extradata_list = self.extract_from_page(topic, 'col-md-12', 'h3')
                elif title in faq['h2_header']:
                    contain_url_list, q_list, a_list, extradata_list = self.extract_from_page_bolded_questions(topic, 'col-md-12', 'h2')
                else:
                    raise Exception('Unable to parse FAQ')

                for contain_url, q, a, extradata in zip(contain_url_list, q_list, a_list, extradata_list):
                    Schema(topic, self.sourcedate, contain_url, self.response_auth, q, a, extradata)
                    """
                    TODO: dump schema into jsonl
                    """
                    
            # pp = pprint.PrettyPrinter(indent=4)
            # pp.pprint(info_list_[-3:])

            # with jsonlines.open('./data/CDC_v0.1-1.jsonl', 'w') as writer:
            #     writer.write_all(self.link_info)

        except KeyError:
            pass


if __name__== '__main__':

    crw = Crawler()

    # crw.topic_integrate(crw.left_topics)
    # crw.topic_integrate(crw.right_topics)
    # crw.sub_topic_QA(crw.link_info)
    crw.other_QA()

    # print(crw.link_info)
