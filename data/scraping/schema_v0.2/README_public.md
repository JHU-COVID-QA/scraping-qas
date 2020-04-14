# Scraped data

`scraped.tsv` contains 1344 question and answers scraped from 36 unique urls (1329 of these questions have answers)

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

