# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.
"""
CDC crawler
Expected page to crawl is
https://www.cdc.gov/coronavirus/2019-ncov/faq.html
"""
__author__ = "Seolhwa Lee"
__copyright__ = "Copyright 2020, Johns Hopkins University"
__credits__ = ["Seolhwa Lee", "Darius Irani"]
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "JHU-COVID-QA"
__email__ = "covidqa@jhu.edu"
__status__ = "Development"

import datetime
import time
import json
import pprint
import subprocess
import uuid
from urllib.request import urlopen
from bs4 import BeautifulSoup, NavigableString, CData, Tag
import re


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
        # str (if it is at JHU to know who the answer came from)
        topic['responseAuthority'] = self.response_auth_
        topic['questionUUID'] = str(uuid.uuid1())
        topic['answerUUID'] = str(uuid.uuid1())
        topic['exampleUUID'] = str(uuid.uuid1())
        topic['questionText'] = self.question_
        topic['answerText'] = self.answer_
        topic['hasAnswer'] = True
        topic['targetEducationLevel'] = 'NA'
        topic['extraData'] = self.extradata_


class Crawler():
    def __init__(self):
        url = 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html'
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")

        respons_auth = soup.find(
            'div', class_='d-none d-lg-block content-source')
        soup_ = MyBeautifulSoup(str(respons_auth), 'lxml')
        respons_auth = soup_.get_text()

        self.sourcedate = self.date_cal(soup)
        self.link_info = []
        self.response_auth = respons_auth
        self.url = url

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
        sourcedate = datetime.datetime(
            int(year), int(month), int(day), 0, 0).timestamp()

        return sourcedate

    def target_body(self, url, target_tag: str,
                    target_attr: str, target_attr_string: str):
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")
        topics = soup.find_all(
            target_tag, attrs={
                target_attr: target_attr_string})

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

            self.link_info.append(
                {'topic': topic_name, 'sourceUrl': topic_url})

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

    def get_content_between_blocks(
            self, blocks, header_type, retreieve_questions=False):
        """
        Helper function to get all content in between a specified tag.

        Input:
        - blocks: list of NavigableString that is output to a find_all query
        - header_type: str that is the same tag as the blocks
        - retreieve_questions: bool, if False then content between blocks only contains answers.
                                     if True then content contains mix of questions and answers.

        Output:
        Lists of questions and answers retrieved between the blocks.
        """
        questions = []
        answers = []
        for block in blocks:
            next_node = block.nextSibling
            answer = []
            while next_node is not None:
                if isinstance(next_node, Tag):
                    if not retreieve_questions and next_node.name == header_type:
                        break
                    if retreieve_questions:
                        if next_node.find('strong') and '?' in next_node.find(
                                'strong').get_text():
                            question = next_node.find('strong').get_text()
                            if 'Q:' in question:
                                question = question.split('Q:')[1]
                            questions.append(question)
                        tags = []

                        for tag in next_node.find_all('strong'):
                            if tag.name == 'strong' and '?' in tag.get_text():
                                tag.replaceWith('')
                            if len(next_node.get_text()) > 0:
                                rest = next_node.get_text()
                                if 'A:' in rest:
                                    rest = rest.split('A:')[1]
                                tags.append(rest)
                                current_node = next_node.find_next_siblings(
                                    'p')
                                for curr in current_node:
                                    print("AA==========", curr)
                                    curr_text = curr.get_text()
                                    if curr_text.find('Q:') == -1:
                                        tags.append(curr)
                                    else:  # 'Q:'
                                        if curr_text.find('A:') != -1:
                                            answ_ = curr.contents
                                            print("$$$$$", str(
                                                answ_[-1]).replace("\n", ''))
                                            for a in answ_:
                                                print("#######", a)
                                                if "A:" in a:
                                                    print("@@@@@", a)

                            else:
                                ''' when Q-A <tag> not same level'''
                                # in case of first phrase have 'A:' but,
                                # saparated with 'Q:' level
                                current_node = next_node.find_next('p')
                                # print(current_node)
                                if current_node.contents[0].find('A:') != -1:
                                    # found!
                                    tags.append(
                                        current_node.contents[0].split('A:')[1])
                                else:
                                    tags.append(current_node.contents[0])
                                next_contents = current_node.find_next_siblings(
                                    'p')
                                for content in next_contents:
                                    if content.contents[0].find('Q:') != -1:
                                        break
                                    else:
                                        tags.append(content)

                        if tags:
                            answer.append(tags)

                    else:
                        answer.append(next_node)
                next_node = next_node.nextSibling
                # print("##############", next_node)
            if answer:
                answers.append(answer)
        answers = [answer for answer in answers if answer]
        if retreieve_questions and answers:
            answers = answers[0]
        return questions, answers

    def extract_from_accordian(self, topic, i=1):
        extradata = {}
        url = topic['sourceUrl']
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")

        id_index = 'accordion-' + str(i)
        subtopic_body = soup.find_all('div', id=id_index)

        contain_url_list = []
        q_list = []
        a_list = []
        extradata_list = []
        for sub_topic in subtopic_body:
            questions = sub_topic.find_all('div', class_='card-header')
            answers = sub_topic.find_all('div', class_='card-body')

            for k, (question, answer) in enumerate(
                    zip(questions, answers), start=1):
                soup = MyBeautifulSoup(str(answer), 'lxml')
                a = soup.get_text()
                q = question.get_text()
                # print("question==============", q)
                # print("answer ===============", a)

                if a.find('http') != -1 or a.find('https') != -1:
                    contain_url = True
                else:
                    contain_url = False

                if topic['topic'] == 'Healthcare Professionals and Health Departments':
                    extradata['referenceURL'] = 'https://www.cdc.gov/coronavirus/2019-ncov/hcp/faq.html'
                else:
                    extradata = {}
                contain_url_list.append(contain_url)
                q_list.append(q)
                a_list.append(a)
                extradata_list.append(extradata)
        return contain_url_list, q_list, a_list, extradata_list

    def extract_from_page(self, topic, class_name, header_type, mixed=False):
        extradata = {}
        url = topic['sourceUrl']
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")

        subtopic_body = soup.find_all('div', class_=class_name)

        contain_url_list = []
        q_list = []
        a_list = []
        extradata_list = []
        for sub_topic in subtopic_body:
            blocks = sub_topic.find_all(header_type)
            questions, answers = self.get_content_between_blocks(
                blocks, header_type, mixed)
            # print("q============", questions)
            # print("a============"), answers
            if not mixed:
                questions = blocks

            for question, answer in zip(questions, answers):
                soup = MyBeautifulSoup(
                    ''.join([str(a) for a in answer]), 'lxml')
                a = soup.get_text()
                q = question if mixed else question.get_text()
                # print("========question:", q)
                # print("========answer:", a)
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

    def extract_from_page_with_subtopics(
            self, topic, class_name, header_type, subheader_type):
        extradata = {}
        url = topic['sourceUrl']
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")

        subtopic_body = soup.find_all('div', class_=class_name)

        contain_url_list = []
        q_list = []
        a_list = []
        extradata_list = []
        for sub_topic in subtopic_body:
            subtopics = sub_topic.find_all(header_type)

            subtopic_questions = []
            subtopic_answers = []
            for subtopic in subtopics:
                next_node = subtopic.nextSibling
                question = []
                answer = []
                while next_node is not None:
                    if isinstance(next_node, Tag):
                        if next_node.name == header_type:
                            break
                        bullets = next_node.find_all(subheader_type)
                        questions, answers = self.get_content_between_blocks(
                            bullets, subheader_type, True)
                        if questions:
                            question.append(questions)
                        if answers:
                            answer.append(answers[0])
                    next_node = next_node.nextSibling
                subtopic_questions.append(question)
                subtopic_answers.append(answer)

            if sub_topic.find('a') is not None:
                subtopics = [
                    a.get('title') for a in sub_topic.find_all('a') if a.get('title')]

            for subtopic, questions, answers in zip(
                    subtopics, subtopic_questions, subtopic_answers):
                for q, a in zip(questions, answers):
                    for question, answer in zip(q, a):
                        if 'Respirators' in subtopics:
                            idx = subtopics.index('Respirators')
                        soup = MyBeautifulSoup(
                            ''.join([str(a) for a in answer]), 'lxml')
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
            with open('./data/CDC_main_v0.1.jsonl', 'w') as writer:
                for i, topic in enumerate(info_list, start=len(info_list) + 1):
                    contain_url_list, q_list, a_list, extradata_list = self.extract_from_accordian(
                        topic, i)
                    for contain_url, q, a, extradata in zip(
                            contain_url_list, q_list, a_list, extradata_list):
                        Schema(topic, self.sourcedate, contain_url,
                               self.response_auth, q, a, extradata)
                        json.dump(topic, writer)
                        writer.write('\n')

                    # with jsonlines.open('./data/CDC_v0.1.jsonl', 'w') as writer:
                    #     writer.write_all(topic)

            print("Main page Data saved!")

        except KeyError:
            pass

    def other_QA(self):
        faq = {'accordian': ['Travel', 'K-12 Schools and Childcare Program Administrators',
                             'Community events: for administrators and individuals',
                             'Retirement Communities and Independent Living Facilities'],
               'card': ['Pregnant Women and COVID-19', 'Water Transmission'],
               'Personal Protective Equipment': ['Personal Protective Equipment'],
               'QA': ['Laboratory Biosafety', 'Healthcare Professionals', 'Laboratory Diagnostic Panels'],
               'Healthcare Infection': ['Healthcare Infection']}
        topics_ = self.target_body(
            self.url, 'div', 'class', 'card-body bg-quaternary')
        titles_ = [topic for topic in [topic.text for topic in topics_][0].split('\n') if
                   topic]
        info_list_ = self.topic_integrate(topics_)
        info_list_ = [info for info in info_list_ if info['topic'] in titles_]
        # try:
        with open('./data/CDC_other_v0.1.jsonl', 'w') as writer:
            for title, topic in zip(titles_, info_list_):
                print(title)
                if title in faq['accordian']:
                    """ TODO: figure out how to automate detection
                    also need to check one by one """
                    contain_url_list, q_list, a_list, extradata_list = self.extract_from_accordian(
                        topic)

                elif title in faq['card']:
                    ''' TODO: Water Transmission dosen't work'''
                    contain_url_list, q_list, a_list, extradata_list = self.extract_from_page(topic, 'card-body', 'h4',
                                                                                              False)
                elif title in faq['Healthcare Infection']:
                    contain_url_list, q_list, a_list, extradata_list = self.extract_from_page(topic, 'col-md-12', 'h4',
                                                                                              False)

                elif title in faq['Personal Protective Equipment']:
                    contain_url_list, q_list, a_list, extradata_list = self.extract_from_page_with_subtopics(topic,
                                                                                                             'col-md-12',
                                                                                                             'h2', 'li')

                else:
                    raise Exception('Unable to parse FAQ')

                for contain_url, q, a, extradata in zip(
                        contain_url_list, q_list, a_list, extradata_list):
                    Schema(topic, self.sourcedate, contain_url,
                           self.response_auth, q, a, extradata)
                    print(topic)
                    '''TODO: skip faq['QA'] also check pages one by one'''
                    # json.dump(topic, writer)
                    # writer.write('\n')

            # if title in faq['QA'][0]:
            #     for contain_url, q, a, extradata in zip(contain_url_list, q_list, a_list, extradata_list):
            #         Schema(topic, self.sourcedate, contain_url, self.response_auth, q, a, extradata)
                    # print(topic)


if __name__ == '__main__':
    # ''' sub_topicQA: cdc main page crawler
    # '''
    crw = Crawler()

    ''' for the CDC main page'''
    crw.topic_integrate(crw.left_topics)
    crw.topic_integrate(crw.right_topics)
    crw.sub_topic_QA(crw.link_info)

    ''' for the CDC other frequently QA'''
    crw.other_QA()

    ''' for the FAQs_HP '''
    # subprocess.call("python3 FAQs_HP.py", shell=True)

    ''' for Laboratoey diagnostic panels and laboratory biosafety'''
    # subprocess.call("python3 crawl_lab.py", shell=True)

    ''' Merge all '''
    subprocess.call("cat ./data/CDC_main_v0.1.jsonl ./data/CDC_other_v0.1.jsonl ./data/CDC_FAQs_HP_v0.1.jsonl "
                    "./data/CDCLab_v0.1.jsonl > ./data/CDC_test_v0.1.jsonl", shell=True)
