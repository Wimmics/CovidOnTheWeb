#!/bin/bash
#
# This script runs Morph-xR2RML to produce the RDF version of the CORD19 metadata.csv file
#
# Input argument:
# - arg1: RDF dataset name e.g. "dataset-1-0"
# - arg2: the MongoDB collection to query, e.g. cord19_csv
# - arg3: type of metadata: one of pmcid or sha
# - arg4: xR2RML template mapping file
#
# Author: F. Michel, UCA, CNRS, Inria

XR2RML=$HOME/xR2RML

help()
{
  exe=$(basename $0)
  echo "Usage: $exe <dataset name> <MongoDB collection name> <pmcid|sha> "
  echo "Example:"
  echo "   $exe  dataset-1-0  cord19_csv  sha  xr2rml_cord19_csv_sha_tpl.ttl"
  exit 1
}

# --- Read input arguments
dataset=$1
if [[ -z "$dataset" ]] ; then help; fi

collection=$2
if [[ -z "$collection" ]] ; then help; fi

type=$3
if [[ -z "$type" ]] ; then help; fi

mappingTemplate=$4
if [[ -z "$mappingTemplate" ]] ; then help; fi


# --- Init log file
mkdir $XR2RML/logs &> /dev/null
log=$XR2RML/logs/run_xr2rml_${collection}.log
echo -n "" > $log

# --- Substitute placeholders in the xR2RML template file
mappingFile=/tmp/xr2rml_$$.ttl
awk "{ gsub(/{{dataset}}/, \"$dataset\"); \
       gsub(/{{collection}}/, \"$collection\"); \
       print }" \
    $XR2RML/${mappingTemplate} > $mappingFile
echo "-- xR2RML mapping file --" >> $log
cat $mappingFile >> $log


echo "--------------------------------------------------------------------------------------" >> $log
date  >> $log
java -Xmx4g \
     -Dlog4j.configuration=file:$XR2RML/log4j.properties \
     -jar "$XR2RML/morph-xr2rml-dist-1.1-RC2-jar-with-dependencies.jar" \
     --configDir $XR2RML \
     --configFile xr2rml.properties \
     --mappingFile $mappingFile \
     --output $XR2RML/output_${collection}_${type}.ttl \
     >> $log
date >> $log

rm -f $mappingFile
