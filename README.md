# scraping-qas
This repo deals with webscraping Frequently Asked Questions (FAQs). The goal is to scrape data from trusted source and store the data in our 
[schema](https://github.com/JHU-COVID-QA/scraping-qas/wiki/Schema-v0.1).
Another group will then deal with the NLP to make this data useful.

## Setup

Run `conda env create -f environment.yml` to setup the conda environment with the correct configurations.
This project uses python3.6. 

Make sure to then run `python setup.py install`. This will create a local library called `covid_scraping` that you will use.

### Installing dependenceis

Use conda to install dependencies

### Updating the conda env

If you installed new dependencies, run `conda env export --from-history --ignore-channel > environment.yml`
and then push the new `environment.yml` configuration file


## Websites to scrape

We have a list of websites to scrape. Please choose one of the websites from our [todo list](https://github.com/JHU-COVID-QA/scraping-qas/projects/1).

### Scraping a new website
Once you have claimed a website to work on, move it from the todo column to the in progress column on our [board](https://github.com/JHU-COVID-QA/scraping-qas/projects/1)
and assign yourself to the issue corresponding to the website.

Next, create a new subdirectory under `src/` where you will put all of your code to scrape Questions and Answers from the website you chose.
Also, please make a new branch where you will work on. The name of the branch should be the same name as the new subdirectory you just made.

A good place to start is to adapt a scraper from [deepset-ai/COVID-QA](https://github.com/deepset-ai/COVID-QA/tree/master/datasources/scrapers). Note they use scrapy, while we use BeautifulSoup for most of our scripts. It's up to you which packages you use, but please update the conda environment if you add dependencies.

### Converting the scraped QAs to our schema
This code snippet gives an example of creating a dictionary based on our [schema](https://github.com/JHU-COVID-QA/scraping-qas/wiki/Schema-v0.1).
**TODO:** add code snippet

### Storing the scraped data
Once you converted the scraped data into the format specified by our schema, please store your data in the same subdirectory you created. The data should be stored as jsonl - that is one json object per line. 
Use the following naming convention: `<Source>_<schema_version>.jsonl`. So `CDC_v0.1.json` will refer to data scraped from the CDC website and stored under the v0.1 schema

### Testing your stored data
At this point, just run `covid_scraping.test_jsonlines('<Source>_<schema_version>.jsonl')`. If you see any error messages, that means your data was not stored correctly according to our schema

Here is an [example]() of how to use this function.


Once you get to this point, please make a pull request and assign the pull request to @azpoliak and @dr-irani.
