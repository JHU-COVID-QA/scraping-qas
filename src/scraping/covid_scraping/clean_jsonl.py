import argparse
import jsonlines
import json
from bs4 import BeautifulSoup


def get_args():
    parser = argparse.ArgumentParser(description="Scrape resources from Medicaid.")
    parser.add_argument('jsonl', help='jsonl file to clean', type=str)

    args = parser.parse_args()
    return args

def remove_links(soup, extra_data):
    if soup.find('a'):
        links = [(link.text, link.get('href')) for link in soup.find_all('a')]
        extra_data[question.get_text()] = links
    return soup.get_text(), extra_data

def clean_jsonl():
    args = get_args()
    lines = []
    with jsonlines.open(args.jsonl) as reader:
        for line in reader:
            lines.append(line)

    for line in lines:
        question_soup = BeautifulSoup(line['questionText'], 'lxml')
        answer_soup = BeautifulSoup(line['answerText'], 'lxml')
        extra_data = line['extraData']
        question, extra_data = remove_links(question_soup, extra_data)
        answer, extra_data = remove_links(answer_soup, extra_data)
        line['questionText'] = question
        line['answerText'] = answer
        line['extraData'] = extra_data


    filename = args.jsonl.split('.jsonl')[0] + '_cleaned.jsonl'
    with open(filename, 'w') as writer:
        for line in lines:
            json.dump(line, writer)
            writer.write('\n')


if __name__ == '__main__':
    clean_jsonl()
