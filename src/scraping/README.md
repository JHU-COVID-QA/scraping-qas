# Scraping Frequently Asked Questions

This subdirectory deals with webscraping Frequently Asked Questions (FAQs). The goal is to scrape data from trusted source and store the data in our [schema](https://github.com/jsedoc/Covid-19-infobot/wiki/Schema-v0.1). Another group will then deal with the NLP to make this data useful.

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

We have a list of websites to scrape. Please choose one of the websites from our [todo list](https://github.com/jsedoc/Covid-19-infobot/projects/3).

### Scraping a new website
Once you have claimed a website to work on, move it from the todo column to the in progress column on our [board](https://github.com/jsedoc/Covid-19-infobot/projects/3) and assign yourself to the issue corresponding to the website.

Next, create a new subdirectory here where you will put all of your code to scrape Questions and Answers from the website you chose.

### Converting the scraped QAs to our schema
This code snippet gives an example of creating a dictionary based on our [schema](https://github.com/jsedoc/Covid-19-infobot/wiki/Schema-v0.1).

https://github.com/jsedoc/Covid-19-infobot/blob/0a4ae016e050dd4de0ee516ae7cfc0c119cf9723/src/scraping/internalCOVIDinfoSheet/internalQAs2schema.py#L5-L27

### Storing the scraped data
Once you converted the scraped data into the format specified by our schema, please store your data under `data/scraping` from the root of the repo. The data should be stored as jsonl - that is one json object per line. 
Use the following naming convention: `<Source>_<schema_version>.jsonl`. So `CDC_v0.1.json` will refer to data scraped from the CDC website and stored under the v0.1 schema

### Testing your stored data
At this point, just run `covid_scraping.test_jsonlines('<Source>_<schema_version>.jsonl')`. If you see any error messages, that means your data was not stored correctly according to our schema

Here is an [example](https://github.com/jsedoc/Covid-19-infobot/blob/2e187c8295fb02f2666111fc33bc34d1eac2563f/src/scraping/internalCOVIDinfoSheet/internalQAs2schema.py#L39) of how to use this function.


Once you get to this point, please ping @ctongfei on your issue so he knows the data is ready for him.

