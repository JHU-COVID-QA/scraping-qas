import datetime, time
import pprint
import uuid
from urllib import request, response, error, parse
from urllib.request import urlopen
from bs4 import BeautifulSoup, NavigableString, CData, Tag
import json
import jsonlines

from covid_scraping import test_jsonlines

'''
<div class="sf-content-block content-block" >
    <div ><h2></h2><h2><strong>COVID-19 virus can be transmitted in areas with hot and humid climates <o:p></o:p></strong></h2><p>From the
evidence so far, the COVID-19 virus can be transmitted in ALL AREAS, including areas with
hot and humid weather. Regardless of climate, adopt protective measures if you
live in, or travel to an area reporting COVID-19. The best way to
protect yourself against COVID-19 is by frequently cleaning your hands. By
doing this you eliminate viruses that may be on your hands and avoid infection
that could occur by then touching your eyes, mouth, and nose.<o:p></o:p></p><p>&nbsp;</p></div>

</div>

Unfortunately, the "sf-content-block" has a lot of other times it is used but are not questions. I naively look for <h2> which is a bolded question

Originally written by @KentonMurray so direct questions to him

'''



class Crawler():
    def __init__(self):

        url = 'https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters'
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")

        qas_plus_some = soup.find_all('div', class_='sf-content-block content-block')

        qa_pairs = []
        #print(qas_plus_some)
        for potential in qas_plus_some:
            #print(potential)
            for child in potential.children:
                #print(child)
                if "h2" in str(child): # Super hacky ... but this seemed to be the best way for this site
                    s_child = str(child)
                    s_child = s_child.replace("\n", " ")
                    s_child = s_child.replace(u'\xa0', u' ')
                    qa = s_child.split("</h2>")
                    if len(qa) == 2:
                        question = qa[0].lstrip("<div><h2>")
                        answer = qa[1].rstrip("</p></div>")
                        answer = answer.lstrip("<p>")
                        answer = answer.replace("</p><p>"," ")
                    elif len(qa) == 3: #First question is different
                        question = qa[1].lstrip("<h2><strong>")
                        question = question.rstrip("<o:p></o:p></strong>")
                        answer = qa[2].lstrip("<p>")
                        answer = answer.rstrip(" </p></div>") 
                        answer = answer.rstrip("<o:p></o:p></p><p>")
                    else:
                        print("ERROR:") #TODO: better error handling?
                    #print("question:", question)
                    #print("answer:", answer)
                    qa_pairs.append((question,answer))
            #print("~~~~~~~~~~~")

        
        #print(qa_pairs)
        #print("~~~~~~~~~~~")

        list_of_json = []
        for pair in qa_pairs:
            timestamp = int(time.time())
            #print(timestamp)
            #print(pair)
            data = {
                "sourceName" : 'WHOMyth',
                "sourceUrl" : 'url',
                "typeOfInfo" : 'QA',
                "dateScraped" : float(timestamp),
                "sourceDate" : float(timestamp),
                "lastUpdateTime" : float(timestamp),
                "needUpdate" :  True,
                "containsURLs" : False, # TODO: need to make logic
                "typeOfInfo" : 'QA',
                "isAnnotated" : False,
                "responseAuthority" : "",
                "questionUUID" : str(uuid.uuid1()),
                "answerUUID" : str(uuid.uuid1()),
                "exampleUUID" : str(uuid.uuid1()),
                "questionText" : pair[0],
                "answerText" : pair[1],
                "hasAnswer" : True,
                "targetEducationLevel" : 'NA',
                "topic" : "Myths",
                "extraData" : {}

            }
            list_of_json.append(data)

        #print("list_of_json:", list_of_json)
        self.list_of_json = list_of_json

    def write_jsonl(self):
        try:
            # pp = pprint.PrettyPrinter(indent=4)
            # pp.pprint(info_list[-9:])

            with jsonlines.open('../../../data/scraping/WHOMyth_v0.1.jsonl', 'w') as writer:
                writer.write_all(self.list_of_json)

        except KeyError:
            pass
        


if __name__== '__main__':

    crw = Crawler()
    crw.write_jsonl()
    test_jsonlines('../../../data/scraping/WHOMyth_v0.1.jsonl')

