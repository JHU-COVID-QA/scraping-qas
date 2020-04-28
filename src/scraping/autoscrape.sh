#!/bin/bash

#This script reruns all of the scrapers.
#It is dependant on conda and having a github deploy key configured
#It also requires that the public spreadsheet is avalable at the url in the script

base_dir=$(echo "/home/ubuntu/autoscraper")
log_file=$(date +"/home/ubuntu/autoscraper/src/scraping/autoscrape_logs/autoscrape-%b-%d-%H.log")
cd $base_dir/src/scraping

branch_name=$(date +"autoscrape-test-%b-%d-%H")

git stash
git checkout master
git pull
git checkout -b $branch_name &>> $log_file

eval "$(/home/ubuntu/anaconda3/bin/conda shell.bash hook)" &>> $log_file
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh &>> $log_file
conda env update  --file environment.yml  --prune &>> $log_file
conda activate crawler &>> $log_file
python setup.py install &>> $log_file


cd $base_dir/src/scraping/scrapers
wget --no-check-certificate -O COVID19infosheet\ -\ Info.tsv  "https://docs.google.com/spreadsheets/d/1Drmwo62V4MvB1X6eTwi1L-f3EYq09oocQ2Jvo-XR1TQ/export?gid=0&format=tsv" &>> $log_file
python scrape_all.py &>> $log_file
python deepsetAI_scraper.py &>> $log_file 
python make_public.py --path $base_dir/data/scraping/schema_v0.2/

cd $base_dir/data/scraping
git add schema_v0.1/* schema_v0.2/*  &>> $log_file
git commit -m $(date +"autoscrape-%b-%d-%H") &>> $log_file
git push --set-upstream origin $branch_name &>> $log_file

cd $base_dir/src/scraping
python log_to_json.py $log_file
curl -X POST -H 'Content-type: application/json' --data @tmp.json  https://hooks.slack.com/services/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
rm tmp.json

