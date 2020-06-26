import os
import json
import pandas as pd

def main():
  path="schema_v0.3/"
  source2stats = {}
  for filename in os.listdir(path):
    answer_count, question_count = 0, 0
    print(filename)
    if filename.endswith(".jsonl"):
      for line in open(path+filename):
        obj = json.loads(line)
        if obj['sourceName'] not in source2stats:
          source2stats[obj['sourceName']] = [0, 0]
        if obj['answerText']:
          answer_count += 1
          source2stats[obj['sourceName']][1] += 1
        if obj['questionText']:
          question_count += 1
          source2stats[obj['sourceName']][0] += 1
    #source2stats[filename.split("_v0.3")[0]] = (question_count, answer_count)

  print(source2stats)
  df = pd.DataFrame.from_dict(source2stats).T
  df = df.rename(columns={0: "questions", 1: "answers"})
  tot_qs = sum(df['questions'])
  tot_as = sum(df['answers'])
  f_out = open("scraped_stats.md", "w")
  tab = df.to_markdown().split("\n")
  tab.insert(2, "| **total**                         |          **%d** |       **%d** |" % (tot_qs, tot_as))
  f_out.write("\n".join(tab))
  f_out.close()

if __name__ == '__main__':
  main()
