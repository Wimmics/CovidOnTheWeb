#!/bin/bash
#
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria

version=1.2
dash_version=1-2
date=2020-11-05
triples=1372643149

temp=/tmp/temp_$$.ttl
awk "{ gsub(/{{dash-version}}/, \"$dash_version\"); \
       gsub(/{{version}}/, \"$version\"); \
       gsub(/{{date}}/, \"$date\"); \
       print }" \
    cord19-metadata-dataset_tpl.ttl > cord19-metadata-dataset.ttl

temp=/tmp/temp_$$.ttl
awk "{ gsub(/{{dash-version}}/, \"$dash_version\"); \
       gsub(/{{triples}}/, \"$triples\"); \
       print }" \
    cord19-metadata-dataset-void_tpl.ttl > cord19-metadata-dataset-void.ttl
