# Scraping Frequently Asked Questions

This subdirectory deals with webscraping Frequently Asked Questions (FAQs). The goal is to scrape data from trusted source and store the data in our [schema](https://github.com/jsedoc/Covid-19-infobot/wiki/Schema-v0.1). Another group will then deal with the NLP to make this data useful.

## Setup

Run `conda env create -f environment.yml` to setup the conda environment with the correct configurations.
This project uses python3.6. 

Make sure to then run `python setup.py install`. This will create a local library called `covid_scraping` that you will use.

### Installing dependenceis

Use conda to install dependencies

### Updating the conda env

If you installed new dependencies, run `conda env export --from-history --ignore-channel > environment.yml.tmp`.
Now, merge `environment.yml.tmp` and `environment.yml` into `environment.yml` so that you do not overwrite other
dependencies in the yml file.
Finally, push the new `environment.yml` configuration file


## Websites to scrape

We have a list of websites to scrape. Please choose one of the websites from our [todo list](https://github.com/jsedoc/Covid-19-infobot/projects/3).

### Scraping a new website
Once you have claimed a website to work on, move it from the todo column to the in progress column on our [board](https://github.com/jsedoc/Covid-19-infobot/projects/3) and assign yourself to the issue corresponding to the website.

Next, create a new branch using
`git checkout -b <name-of-new-branch` where the branch name should be `scraping-<name of website`.
You will implement your scraper in a new file in https://github.com/jsedoc/Covid-19-infobot/tree/master/src/scraping/scrapers.
Please name the new file the name of the website you are scraping, so if you are scraping FAQs from the World Health Organization, the filename should be `who.py`. 

#### Implementing Scraper clas
All your code needs to do is implement the [Scraper abstract class](https://github.com/jsedoc/Covid-19-infobot/blob/2f427fa618873e7e2025bdb86bd8bfdaf2fd61b2/src/scraping/covid_scraping/scraper.py#L17-L31).

Look at [example_scraper](https://github.com/jsedoc/Covid-19-infobot/blob/master/src/scraping/scrapers/example_scraper.py) on how to implement the `scrape()` function.

**TODO for ADAM**: update instructions on scraping


#### Code styling
Before you are finished, make sure that your code abides by our coding style. We use standard [pep8](https://www.python.org/dev/peps/pep-0008/). Run `pep8 <python file name>`. Please fix all style comments (except for line length, and "module level import not at top of file").

Once you get to this point, please make a pull request and assign the pull request to @azpoliak.

## Re-running scrapers
At least once a day, we will re-run all the developed scrapers to added updated FAQs from each scraper.
This will be done by running `scrapers/scrape_all.py`
