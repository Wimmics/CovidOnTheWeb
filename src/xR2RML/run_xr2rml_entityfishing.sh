#!/bin/bash
#
# This script instantiates an xR2RML template file and runs Morph-xR2RML
# to produce the RDF annotations yield by Entity-Fishing.
#
# Input argument:
# - arg1: RDF dataset name e.g. "dataset-1-0"
# - arg2: article part about which to produce annotations. One of title, abstract or body_text
#
# Author: F. Michel, UCA, CNRS, Inria


# MongoDB collection where to read documents
collection=entityfishing_light

# xR2RML template mapping file
mappingTemplate=xr2rml_entityfishing_tpl.ttl


XR2RML=$HOME/xR2RML

help()
{
  exe=$(basename $0)
  echo "Usage: $exe <dataset name> [title|abstract|body_text]"
  echo "Example:"
  echo "   $exe dataset-01 abstract"
  exit 1
}

# --- Read input arguments
dataset=$1
if [[ -z "$dataset" ]] ; then help; fi

articlepart=$2
if [[ -z "$articlepart" ]] ; then help; fi

# --- Init log file
mkdir logs &> /dev/null
log=logs/run_xr2rml_${collection}.log
echo -n "" > $log

# --- Substitute placeholders in the xR2RML template file
mappingFile=/tmp/xr2rml_$$.ttl
awk "{ gsub(/{{dataset}}/, \"$dataset\"); \
       gsub(/{{articlepart}}/, \"$articlepart\"); \
       gsub(/{{collection}}/, \"$collection\"); \
       print }" \
    $XR2RML/${mappingTemplate} > $mappingFile
echo "-- xR2RML mapping file --" >> $log
cat $mappingFile >> $log


echo "--------------------------------------------------------------------------------------" >> $log
date  >> $log
java -Xmx16g \
     -Dlog4j.configuration=file:$XR2RML/log4j.properties \
     -jar "$XR2RML/morph-xr2rml-dist-1.1-RC2-jar-with-dependencies.jar" \
     --configDir . \
     --configFile xr2rml.properties \
     --mappingFile $mappingFile \
     --output output_${collection}_${articlepart}.ttl \
     >> $log
date >> $log

rm -f $mappingFile
