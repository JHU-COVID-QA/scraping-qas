# Scraped data

`scraped.tsv` contains 1399 question and answers scraped from 36 unique urls (1399 of these questions have answers)

## headers in tsv
The headers in the tsv are:

- `sourceUrl` - the URL where the question and answer came from
- `sourceName` - the name of the source
- `dateScraped` - POSIX time of when the data was last scraped
- `sourceDate` - POSIX time of when the data was posted,
- `ID` - ID for the question-answer pair, IDs are the sourceName concatenated with a hast of the question
- `question` - the cleaned text of the question (html tags remove)
- `answer` - the cleaned text of the answer (html tags remove)
- `hasAnswer` - boolean indicating whether the question has an answer

## Stats

These are stats for how many questions-answers we have for our sources
in English

|                                                    |   |
|:---------------------------------------------------|-------------:|
| NYTimes                                            |          102 |
| CNN                                                |           74 |
| FDA                                                |           67 |
| FHM, Folkhälsomyndigheten                          |           62 |
| European Centre for Disease Prevention and Control |           42 |
| Johns Hopkins Bloomberg School of Public Health    |           38 |
| Cleveland Clinic                                   |           32 |
| Public Health Agency of Canada                     |           28 |
| National Foundation for Infectious Diseases        |           27 |
| FloridaGov                                         |           23 |
| World Health Organization (WHO)                    |           23 |
| WHOMyth                                            |           19 |
| UNICEF                                             |           16 |
| JHU HUB                                            |           13 |
| Texas Human Resources                              |           11 |
| Center for Disease Control and Prevention (CDC)    |            9 |
