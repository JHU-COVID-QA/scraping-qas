# Scraping 

This subdirectory deals with webscraping. The goal is to scrape data from trusted source and store the data in our [schema](https://github.com/jsedoc/Covid-19-infobot/wiki/Schema-v0.1)

## Setup

Run `conda env create -f environment.yml` to setup the conda environment with the correct configurations.
This project uses python3.6

### Installing dependenceis

Use conda to install dependencies

### Updating the conda env

If you installed new dependencies, run `conda env export --from-history --ignore-channel > environment.yml`
and then push the new `environment.yml` configuration file


## Websites to scrape

We have a list of websites to scrape. Please choose one of the websites from our [todo list](https://github.com/jsedoc/Covid-19-infobot/projects/3).
Once you have claimed a website to work on, move it from the todo column to the in progress column on our [board](https://github.com/jsedoc/Covid-19-infobot/projects/3) and assign yourself to the issue corresponding to the website
