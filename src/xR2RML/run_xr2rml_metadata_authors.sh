#!/bin/bash
#
# This script runs Morph-xR2RML to produce the RDF version of the CORD19 metadata.csv file
#
# Input argument:
# - arg1: the MongoDB collection to query, e.g. cord19_csv
# - arg2: xR2RML template mapping file
# - arg3: output file name
#
# Author: F. Michel, UCA, CNRS, Inria

XR2RML=.
JAR=$XR2RML/morph-xr2rml-dist-1.3-SNAPSHOT-jar-with-dependencies.jar

help()
{
  exe=$(basename $0)
  echo "Usage: $exe <MongoDB collection name> <xR2RML mapping template> <output file name>"
  echo "Example:"
  echo "   $exe  cord19_json_light  xr2rml_metadata_authors_tpl.ttl  cord19-articles-metadata-authors.ttl"
  exit 1
}

# --- Read input arguments
collection=$1
if [[ -z "$collection" ]] ; then help; fi

mappingTemplate=$2
if [[ -z "$mappingTemplate" ]] ; then help; fi

output=$3
if [[ -z "$output" ]] ; then help; fi


# --- Init log file
mkdir $XR2RML/logs &> /dev/null
log=$XR2RML/logs/run_xr2rml_${collection}_authors.log
echo -n "" > $log

# --- Substitute placeholders in the xR2RML template file
mappingFile=/tmp/xr2rml_$$.ttl
awk "{ gsub(/{{collection}}/, \"$collection\"); \
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
     --configFile xr2rml.properties \
     --mappingFile $mappingFile \
     --output $output \
     >> $log
date >> $log

rm -f $mappingFile
