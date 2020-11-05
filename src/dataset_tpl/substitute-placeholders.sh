#!/bin/bash
#
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria

# CORD19 and Covid-on-the-Web environment definitions
. ../env.sh

# Update the metadata about the Covid-on-the-Web dataset
date=2020-11-05
no_triples=1372643149
doi=10.5281/zenodo.4247134


temp=/tmp/temp_$$.ttl
awk "{ gsub(/{{dash-version}}/, \"$COTW_VERSION_DASH\"); \
       gsub(/{{version}}/, \"$COTW_VERSION\"); \
       gsub(/{{date}}/, \"$date\"); \
       gsub(/{{cord19version}}/, \"$CORD19_VERSION\"); \
       gsub(/{{cord19date}}/, \"$CORD19_DATE\"); \
       print }" \
    cord19-metadata-dataset_tpl.ttl > cord19-metadata-dataset.ttl

temp=/tmp/temp_$$.ttl
awk "{ gsub(/{{dash-version}}/, \"$COTW_VERSION_DASH\"); \
       gsub(/{{triples}}/, \"$no_triples\"); \
       gsub(/{{doi}}/, \"$doi\"); \
       print }" \
    cord19-metadata-dataset-void_tpl.ttl > cord19-metadata-dataset-void.ttl
