#!/bin/bash
#
# Author: F. Michel, UCA, CNRS, Inria

dataset=dataset-1-0
version=1.0
date=2020-04-06
triples=10

temp=/tmp/temp_$$.ttl
awk "{ gsub(/{{dataset}}/, \"$dataset\"); \
       gsub(/{{version}}/, \"$version\"); \
       gsub(/{{date}}/, \"$date\"); \
       print }" \
    cord19-nekg-metadata_tpl.ttl > cord19-nekg-metadata.ttl

temp=/tmp/temp_$$.ttl
awk "{ gsub(/{{dataset}}/, \"$dataset\"); \
       gsub(/{{triples}}/, \"$triples\"); \
       print }" \
    cord19-nekg-metadata-void_tpl.ttl > cord19-nekg-metadata-void.ttl
