import argparse
import jsonlines
import json
from bs4 import BeautifulSoup
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
from covid_scraping.test_dump_to_schema import check_keys, check_values


def _get_args():
    parser = argparse.ArgumentParser(
        description="Scrape resources from Medicaid.")
    parser.add_argument('jsonl', help='jsonl file to clean', type=str)

    args = parser.parse_args()
    return args


def _remove_links(line, field):
    nlp = English()
    extra_data = line['extraData']
    soup = BeautifulSoup(extra_data['original_' + field], 'lxml')
    matcher = PhraseMatcher(line[field].vocab)

    link_dict = {}
    if soup.find('a'):
        for link in soup.find_all('a'):
            matcher = PhraseMatcher(line[field].vocab)
            matcher.add('HYPERLINK', None, *[nlp.make_doc(link.text)])
            matches = matcher(line[field])
            for _, start, end in matches:
                link_dict[str((start, end))] = link.get('href')

    fieldname = field.split('Text')[0] + 'Links'
    extra_data[fieldname] = link_dict
    line['extraData'] = extra_data


def _clean_element(line, field):
    soup = BeautifulSoup(line[field], 'lxml')
    extra_data = line['extraData']
    extra_data['original_' + field] = line[field]
    line[field] = soup.get_text().strip()
    line['extraData'] = extra_data


def _tokenize_element(line, field):
    nlp = English()
    """
    Opting to create tokenizer that includes English punctuation rules and exceptions.
    If tokenizer with just English vocab desired, use:
    tokenizer = Tokenizer(nlp.vocab)
    """
    tokenizer = nlp.Defaults.create_tokenizer(nlp)

    extra_data = line['extraData']
    tokens = tokenizer(line[field])
    line[field] = tokens
    line['extraData'] = extra_data


def clean_jsonl(filename):
    with jsonlines.open(filename) as reader:
        lines = [line for line in reader]

    for line in lines:
        for field in ['questionText', 'answerText']:
            _clean_element(line, field)
            _tokenize_element(line, field)
            _remove_links(line, field)
            line[field] = ' '.join([token.text for token in line[field]])

    for idx, obj in enumerate(lines):
        check_keys(idx, obj)
        check_values(idx, obj)

    _dump(filename, lines)


def _dump(filename, lines):
    filename = filename.split('.jsonl')[0] + '_cleaned.jsonl'
    with open(filename, 'w') as writer:
        for line in lines:
            json.dump(line, writer)
            writer.write('\n')


if __name__ == '__main__':
    args = _get_args()
    clean_jsonl(args.jsonl)
