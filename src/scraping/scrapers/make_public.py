import os
import argparse
import json
import pandas as pd

def get_args():
    parser = argparse.ArgumentParser(description='Make one public tsv file for release')
    parser.add_argument('--path', type=str, default="",
                        help='Path to directory of jsonl files to release')
    

    args = parser.parse_args()
    print(args)
    return args

def main():
    args = get_args()
    # dict_keys(['sourceUrl', 'sourceName', 'dateScraped', 'sourceDate', 
    #'lastUpdateTime', 'needUpdate', 'containsURLs', 'typeOfInfo', 'isAnnotated', 
    #'responseAuthority', 'questionUUID', 'answerUUID', 'exampleUUID', 'questionText', 
    #'answerText', 'hasAnswer', 'targetEducationLevel', 'topic', 'extraData'])

    #Index(['sourceUrl', 'sourceName', 'sourceDate', 'hasAnswer', 'targetLocation',
    #   'language', 'dateScraped', 'questionOriginal', 'questionText',
    #   'answerOriginal', 'answerText', 'questionUUID', 'answerUUID', 'ID',
    #   'answerContainsURLs', 'answerToks2URL'],

    data = []
    for filename in os.listdir(args.path):
        if filename.endswith("jsonl"):
            if "internal" in filename:
                continue
            for line in open(args.path + "/" + filename):
                data.append(json.loads(line))
                
    df = pd.DataFrame(data)
    df['question'] = df['questionText']
    df['answer'] = df['answerText']
    df = df.drop(columns=['needUpdate', 'extraData', 'isAnnotated', 'typeOfInfo',
        'responseAuthority', 'topic', 'targetEducationLevel', 'lastUpdateTime', 'answerOriginal', 'questionOriginal', 
        'questionText', 'answerText', 'answerToks2URL', 'answerContainsURLs', 'answerUUID', 'questionUUID'])
    print("%d unique urls" % len(set(df['sourceUrl'])))
    print("%d number of questions" % df.shape[0])
    print("%d number of answers" % sum(df['hasAnswer']))
    df.to_csv(args.path + "/scraped.tsv" ,sep="\t")

if __name__ == '__main__':
    main()
