#!/usr/bin/env bash

#Exit if an error occurs
set -e

#Go to the project path
cd /root/ideaiweb

if test -f ./databases/data/form.csv; #existe y es un archivo regular
then
    touch ./databases/data/competitive.bib
    touch ./databases/data/non-competitive.bib
else
    echo "You need to provide the form.csv information to this path: ./databases/data/form.csv"
    exit 1
fi

#Download updated list of projects (use -q "quiet" when executing from crond)
# echo "Downloading competitive projects..."
# wget -O ./databases/data/competitive.bib https://futur.upc.edu/bibtex/IDEAI-UPC/as/cGFydGljaXBhY2lvcHJvamVjdGVyZGljb21wZXRpdGl1/a/1
# echo "OK!"
#
# echo "Downloading non-competitive projects..."
# wget -O ./databases/data/non-competitive.bib https://futur.upc.edu/bibtex/IDEAI-UPC/as/cGFydGljaXBhY2lvcHJvamVjdGVyZGlub2NvbXBldGl0aXU=
# echo "OK!"

#Parse and unify with old form inormation
echo "Parsing and unifying with old data..."
./databases/projects.py > ./databases/last_projects_error.log 2>&1
if [ ! -s ./databases/last_projects_error.log ]; then rm -f ./databases/last_projects_error.log; fi
echo "OK!"

#Upload new data to production server
# ./copy_db.sh > ~/Desktop/error_upload_ideai.log 2>&1
# if [ ! -s ~/Desktop/error_upload_ideai.log ]; then rm -f ~/Desktop/error_upload_ideai.log; fi
