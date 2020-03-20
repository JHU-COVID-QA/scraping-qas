# Scraping code

Code for scraping here

## Conda environment

This project uses python3.6

### Setup

Run `conda env create -f environment.yml` to setup the conda environment with the correct configurations.

### Installing dependenceis

Use conda to install dependencies

### Updating the conda env

If you installed new dependencies, run `conda env export --from-history --ignore-channel > environment.yml`
and then push the new `environment.yml` configuration file
