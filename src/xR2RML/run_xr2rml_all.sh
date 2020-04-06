#!/bin/bash
# Author: F. Michel, UCA, CNRS, Inria

dataset=dataset-1-0

./run_xr2rml_entityfishing.sh       $dataset title
./run_xr2rml_entityfishing.sh       $dataset abstract
./run_xr2rml_entityfishing.sh       $dataset body_text

./run_xr2rml_cord19_csv_sha.sh      $dataset cord19_v6_csv
./run_xr2rml_cord19_csv_pmcid.sh    $dataset cord19_v6_csv
