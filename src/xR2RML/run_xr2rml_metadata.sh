#!/bin/bash
#
# This script runs Morph-xR2RML to produce the RDF version of the CORD19 metadata.csv file
#
# Input argument:
# - arg1: RDF dataset name e.g. "dataset-1-0"
# - arg2: the MongoDB collection to query, e.g. cord19_csv
# - arg3: field used as the paper_id: one of pmcid or sha
# - arg4: xR2RML template mapping file
#
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

XR2RML=.
JAR=$XR2RML/morph-xr2rml-dist-1.3-SNAPSHOT-jar-with-dependencies.jar

help()
{
  exe=$(basename $0)
  echo "Usage: $exe <dataset name> <MongoDB collection name> <pmcid|sha> <xR2RML mapping template>"
  echo "Example:"
  echo "   $exe  dataset-1-0  cord19_metadata  sha  xr2rml_metadata_sha_tpl.ttl"
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
     -jar "$JAR" \
     --configDir $XR2RML \
     --configFile xr2rml_uriencode.properties \
     --mappingFile $mappingFile \
     --output $XR2RML/output_${collection}_${type}.ttl \
     >> $log
date >> $log

rm -f $mappingFile
