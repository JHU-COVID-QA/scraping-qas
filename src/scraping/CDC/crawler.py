import datetime, time
import pprint
from urllib import request, response, error, parse
from urllib.request import urlopen
from bs4 import BeautifulSoup, NavigableString, CData, Tag
import jsonlines


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


url = 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html'
html = urlopen(url)
soup = BeautifulSoup(html, "lxml")
# here, the "lxml" is the html parserdsps


left_topics = soup.find_all('ul', class_='col-md-6 float-left list-group list-group-flush')
right_topics = soup.find_all('ul', class_='col-md-6 float-right list-group list-group-flush')
# all_topics = soup.find_all('div', class_='row no-gutters')

# print(left_topics)
# [<ul class="col-md-6 float-left list-group list-group-flush">
# <li class="list-group-item"><a href="#basics">Coronavirus Disease 2019 Basics</a></li>
# <li class="list-group-item"><a href="#spreads">How It Spreads</a></li>
# <li class="list-group-item"><a href="#protect">How to Protect Yourself</a></li>
# <li class="list-group-item"><a href="#symptoms">Symptoms &amp; Testing</a></li> </ul>]

link_info = []

timestamp = int(time.time())
# <span id="last-reviewed-date">March 19, 2020</span>
sourcedate = soup.find('span', id='last-reviewed-date').get_text()

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


def topic_to_url(topic_lists):
    for i, topic in enumerate(topic_lists):
        topic_name = topic.get_text()
        # print(left_topic_name) # Coronavirus Disease 2019 Basics

        topic_lists_link = topic.get('href')
        # print(topic_lists_left_link) # #basics

        topic_url = 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html' + topic_lists_link
        link_info.append({'topic': topic_name, 'sourceUrl': topic_url})


def topic_integrate(topic_):
    '''
     [{'sourceName': 'Coronavirus Disease 2019 Basics',
       'sourceUrl': 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html#basics'},
      {'sourceName': 'How It Spreads', 'sourceUrl: 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html#spreads'},
      {'sourceName': 'How to Protect Yourself',
       'sourceUrl': 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html#protect'},
      {'sourceName': 'Symptoms & Testing', 'sourceUrl': 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html#symptoms'}]
    '''
    # for left_child, right_child in zip(left_topics, right_topics):
    #     topic_lists_left = left_child.find_all('a', href=True)
    #     topic_lists_right = right_child.find_all('a', href=True)
    #     topic_to_url(topic_lists_left)
    #     topic_to_url(topic_lists_right)
    for child in topic_:
        topic_lists = child.find_all('a', href=True)
        topic_to_url(topic_lists)


def sub_topic_QA(info_list):
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
        for i, topic in enumerate(info_list, start=len(info_list)+1):
            # print(i)
            # print(sub_topic) # {'sourceName': 'Coronavirus Disease 2019 Basics', 'sourceUrl': 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html#basics'}
            url = topic['sourceUrl']
            html = urlopen(url)
            soup = BeautifulSoup(html, "lxml")

            # left_topics = soup.find_all('ul', class_='col-md-6 float-left list-group list-group-flush')

            id_index = 'accordion-' + str(i)
            subtopic_body = soup.find_all('div', id=id_index)


            for init, sub_topic in enumerate(subtopic_body, start=1):
                # print(sub_topic)
                # questions = sub_topic.find_all('span', attrs={'aria-level':'1'})
                # questions = sub_topic.find_all('div', id=id_index + '-card-' + str(init))
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
                    # a = answer.get_text()

                    # print(q) # What is a novel coronavirus?
                    # info_list.append({'sub_topic_'+str(k):{'question':q, 'answer':a}})
                    topic['typeOfInfo_'+str(k)] = {'questionText':q, 'answerText':a, 'isAnnotated':'false',
                                                   'questionID':int(k), 'answerID':int(k), 'hasAnswer':'true',
                                                   'containsURLs':'', 'needUpdate':'', 'targetEducationLevel':''}


        # link_info.append({'dateScraped':timestamp, 'sourceName':'CDC', 'sourceDate':datetime.datetime(2020,3,12,0,0).timestamp()})
        link_info.append({'dateScraped': timestamp, 'sourceName': 'CDC',
                          'sourceDate': sourcedate, 'lastUpdateTime': ''})
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(info_list[-2:])
        # print(info_list)

        # return info_list
        # with open('CDC_v0.1.json', 'w') as outfile:
        #     json.dump(link_info, outfile)
        with jsonlines.open('test_v0.1.jsonl', 'w') as writer:
            writer.write_all(link_info)

    except KeyError:
        pass

    # return info_list
    # print(info_list)



if __name__== '__main__':

    topic_integrate(left_topics)
    topic_integrate(right_topics)
    sub_topic_QA(link_info)
