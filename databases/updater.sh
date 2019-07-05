#!/usr/bin/env bash

#Exit if an error occurs
set -e

#Go to the project path
cd /home/ivan/github/ideaiweb

#Download updated list of projects
wget -q -O ./csv/competitive.bib https://futur.upc.edu/bibtex/IDEAI-UPC/as/cGFydGljaXBhY2lvcHJvamVjdGVyZGljb21wZXRpdGl1/a/1
wget -q -O ./csv/non-competitive.bib https://futur.upc.edu/bibtex/IDEAI-UPC/as/cGFydGljaXBhY2lvcHJvamVjdGVyZGlub2NvbXBldGl0aXU=

#Parse and unify with old form inormation
/home/ivan/anaconda3/bin/python3.7 ./databases/Projects.py > ~/Desktop/error_projects_ideai.log 2>&1
if [ ! -s ~/Desktop/error_projects_ideai.log ]; then rm -f ~/Desktop/error_projects_ideai.log; fi

#Upload new data to production server
./copy_db.sh > ~/Desktop/error_upload_ideai.log 2>&1
if [ ! -s ~/Desktop/error_upload_ideai.log ]; then rm -f ~/Desktop/error_upload_ideai.log; fi
