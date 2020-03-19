from urllib import request, response, error, parse
from urllib.request import urlopen
from bs4 import BeautifulSoup, NavigableString, CData, Tag
import json



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

# print(left_topics)
# [<ul class="col-md-6 float-left list-group list-group-flush">
# <li class="list-group-item"><a href="#basics">Coronavirus Disease 2019 Basics</a></li>
# <li class="list-group-item"><a href="#spreads">How It Spreads</a></li>
# <li class="list-group-item"><a href="#protect">How to Protect Yourself</a></li>
# <li class="list-group-item"><a href="#symptoms">Symptoms &amp; Testing</a></li> </ul>]

link_info = []
filter_words = ['icon']

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
                # yield str('<a href="{}"></a>'.format(descendant.get('href', '')))

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
        link_info.append({'topic_name': topic_name, 'topic_url': topic_url})

def topic_integrate():
    '''
     [{'topic_name': 'Coronavirus Disease 2019 Basics',
       'topic_url': 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html#basics'},
      {'topic_name': 'How It Spreads', 'topic_url': 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html#spreads'},
      {'topic_name': 'How to Protect Yourself',
       'topic_url': 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html#protect'},
      {'topic_name': 'Symptoms & Testing', 'topic_url': 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html#symptoms'}]
    '''
    for left_child, right_child in zip(left_topics, right_topics):
        topic_lists_left = left_child.find_all('a', href=True)
        topic_lists_right = right_child.find_all('a', href=True)
        topic_to_url(topic_lists_left)
        topic_to_url(topic_lists_right)

def sub_topic_QA(info_list):
    '''
    Question :
    <div id="accordion-9" class="accordion indicator-plus accordion-white mb-3" role="tablist">
    <div id="accordion-10" class="accordion indicator-plus accordion-white mb-3" role="tablist">
    Answer :
    <div class="card-body bg-gray-l3"><p>A novel coronavirus is a new coronavirus that has not been previously identified. The virus causing coronavirus disease 2019 (COVID-19),
    is not the same as the <a href="/coronavirus/types.html">coronaviruses that commonly circulate among humans</a>&nbsp;and cause mild illness, like the common cold.</p>
    '''
    try:
        for i, topic in enumerate(info_list, start=9):
            # print(sub_topic) # {'topic_name': 'Coronavirus Disease 2019 Basics', 'topic_url': 'https://www.cdc.gov/coronavirus/2019-ncov/faq.html#basics'}
            url = topic['topic_url']
            html = urlopen(url)
            soup = BeautifulSoup(html, "lxml")

            # left_topics = soup.find_all('ul', class_='col-md-6 float-left list-group list-group-flush')

            id_index = 'accordion-' + str(i)
            subtopic_body = soup.find_all('div', id=id_index)

            for sub_topic in subtopic_body:
                # print(sub_topic)
                questions = sub_topic.find_all('span', attrs={'aria-level':'1'})
                answers = sub_topic.find_all('div', class_='card-body bg-gray-l3')

                # print(answers)
                for k, (question, answer) in enumerate(zip(questions, answers)):
                    # print(answer)
                    soup = MyBeautifulSoup(str(answer), 'lxml')
                    q = question.get_text()
                    a = soup.get_text()

                    # print(q) # What is a novel coronavirus?
                    # info_list.append({'sub_topic_'+str(k):{'question':q, 'answer':a}})
                    topic['sub_topic_'+str(k)] = {'question':q, 'answer':a}
        print(info_list)

        return info_list

    except KeyError:
        pass

    # return info_list
    # print(info_list)



if __name__== '__main__':

    topic_integrate()
    sub_topic_QA(link_info)
