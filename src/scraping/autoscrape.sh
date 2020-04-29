#!/bin/bash

#This script reruns all of the scrapers.
#It is dependant on anaconda3 in the home directory and having a github deploy key configured
#It also requires that the public spreadsheet is avalable at the url in the script

date=$(date +"%b-%d-%H")
base_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
log_file=$(date +"$base_dir/autoscrape_logs/autoscrape-$date.log")

branch_name=$(date +"autoscrape-test-$date")

cd $base_dir
git stash &>> $log_file
git checkout master &>> $log_file
git pull &>> $log_file
git checkout -b $branch_name &>> $log_file

eval "$($HOME/anaconda3/bin/conda shell.bash hook)" &>> $log_file
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh &>> $log_file
conda env update  --file environment.yml  --prune &>> $log_file
conda activate crawler &>> $log_file
python setup.py install &>> $log_file


cd $base_dir/scrapers
wget --no-check-certificate -O COVID19infosheet\ -\ Info.tsv  "https://docs.google.com/spreadsheets/d/1Drmwo62V4MvB1X6eTwi1L-f3EYq09oocQ2Jvo-XR1TQ/export?gid=0&format=tsv" &>> $log_file
python scrape_all.py &>> $log_file
python deepsetAI_scraper.py &>> $log_file 
python make_public.py --path $base_dir/../../data/scraping/schema_v0.2/ &>> $log_file

cd $base_dir/../../data/scraping
git add schema_v0.2/*  &>> $log_file
git commit -m $(date +"autoscrape-$date") &>> $log_file
git push origin $branch_name &>> $log_file

cd $base_dir
python log_to_json.py $log_file
curl -X POST -H 'Content-type: application/json' --data @tmp.json https://hooks.slack.com/services/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
rm tmp.json

