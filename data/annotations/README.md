# Aligned and annotated questions

We additionally aligned unanswered questions from Twitter and Qorona with the answered questions in our dataset.
These annotations can found in
`aligned_question_question_answer.csv`

## File structure

The csv file contains the following headers:
```
question1,question2,answer,source,rating
```

- `question1` corresponds to a question from Twitter or Qorona
- `question2` and `answer` are the QA pair from our dataset that a BM25 model aligned with `question1`
- `source` is the source of `question2` and `answer`
- `rating` is a label on a scale from 0 to 100 that indicates how relevant `question2` and `answer` are to `question1`
