#!/bin/bash
# Author: F. Michel, UCA, CNRS, Inria

dataset=dataset-1-0

# Generate articles metadata
./run_xr2rml_metadata.sh   $dataset cord19_metadata sha   xr2rml_metadata_sha_tpl.ttl
./run_xr2rml_metadata.sh   $dataset cord19_metadata pmcid xr2rml_metadata_pmcid_tpl.ttl


# Generate annotations DBpedia Spotlight
./run_xr2rml_annotation.sh $dataset title     spotlight_light     xr2rml_spotlight_tpl.ttl
./run_xr2rml_annotation.sh $dataset abstract  spotlight_light     xr2rml_spotlight_tpl.ttl

# Generate annotations Entity-fishing
./run_xr2rml_annotation.sh $dataset title     entityfishing_light xr2rml_entityfishing_tpl.ttl
./run_xr2rml_annotation.sh $dataset abstract  entityfishing_light xr2rml_entityfishing_tpl.ttl
