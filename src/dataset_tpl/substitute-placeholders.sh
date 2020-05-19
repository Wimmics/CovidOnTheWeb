#!/bin/bash
#
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria

dataset=dataset-1-1
version=1.1
date=2020-05-19
triples=674351000

temp=/tmp/temp_$$.ttl
awk "{ gsub(/{{dataset}}/, \"$dataset\"); \
       gsub(/{{version}}/, \"$version\"); \
       gsub(/{{date}}/, \"$date\"); \
       print }" \
    cord19-metadata-dataset_tpl.ttl > cord19-metadata-dataset.ttl

temp=/tmp/temp_$$.ttl
awk "{ gsub(/{{dataset}}/, \"$dataset\"); \
       gsub(/{{triples}}/, \"$triples\"); \
       print }" \
    cord19-metadata-dataset-void_tpl.ttl > cord19-metadata-dataset-void.ttl
