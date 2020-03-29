#!/bin/bash

# Copyright (c) Johns Hopkins University and its affiliates.
# This source code is licensed under the Apache 2 license found in the
# LICENSE file in the root directory of this source tree.

# Shell script to run all the scrapers with rescrape argument.
# __author__ = "Milind Agarwal"
# __copyright__ = "Copyright 2020, Johns Hopkins University"
# __credits__ = ["Milind Agarwal"]
# __license__ = "Apache 2.0"
# __version__ = "0.1"
# __maintainer__ = "JHU-COVID-QA"
# __email__ = "covidqa@jhu.edu"
# __status__ = "Development"


###########################################################################
###################### STEP 1: RESCRAPE   #################################
###########################################################################
CURDIR=`pwd`

## dialogueMDquestions
echo 'dialogueMDquestions'
cd ../dialogueMDquestions
python dialogueMDquestions2schema.py --rescrape
cd $CURDIR

## AVMA-VET
echo 'AVMA-VET'
cd ../AVMA-vetinary
python scrape_avma.py --rescrape
cd $CURDIR

## NFID
echo 'NFID'
# Added 2>/dev/null because there were exceptions being printed to console.
cd ../NFID
python crawler.py --rescrape 2>/dev/null
cd $CURDIR

## FloridaGov
echo 'FloridaGov'
cd ../FloridaGov
python crawl.py --rescrape
cd $CURDIR

## TexasHR
echo 'TexasHR'
cd ../TexasHumanResources
python crawl.py --rescrape 2>/dev/null
cd $CURDIR

## FDAPrep
echo 'FDAPrep'
cd ../FDA
python crawl.py --rescrape
cd $CURDIR

## WhoMyth
echo 'WhoMyth'
cd ../WHOMyth
python crawler.py --rescrape
cd $CURDIR

## WHO
echo 'WHO'
cd ../WHO
python crawlerWHO.py --rescrape
cd $CURDIR

## CNN
echo 'CNN'
cd ../CNN
python crawler.py --datadir ../../../data/scraping/schema_v0.1/ --rescrape
cd $CURDIR

## Canada Public Health
echo 'Canada Public Health'
cd ../CanadaPublicHealth
python scraper.py --rescrape 2>/dev/null
cd $CURDIR

## NYT
echo 'NYT'
cd ../nytimes
python crawler.py --rescrape 2>/dev/null
cd $CURDIR


python mergeJSONL.py
#################################################################
####################   TODO #####################################
#################################################################
## CDC
# cd ../CDC
# Add code to run scraper
# cd $CURDIR

## ClevelandClinic
# cd ../ClevelandClinic
# python crawl.py --rescrape
# cd $CURDIR

## INTERNAL-COVID
# cd ../internalCOVIDinfoSheet
# python internalQAs2schema.py --rescrape
# cd $CURDIR
