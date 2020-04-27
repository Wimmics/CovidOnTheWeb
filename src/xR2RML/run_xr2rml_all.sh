#!/bin/bash
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria

dataset=dataset-1-1


# Generate articles metadata
./run_xr2rml_metadata.sh   $dataset cord19_metadata sha   xr2rml_metadata_sha_tpl.ttl
./run_xr2rml_metadata.sh   $dataset cord19_metadata pmcid xr2rml_metadata_pmcid_tpl.ttl

./run_xr2rml_metadata_authors.sh cord19_json_light xr2rml_metadata_authors_tpl.ttl


# Generate annotations DBpedia Spotlight
./run_xr2rml_annotation.sh $dataset title     spotlight_light     xr2rml_spotlight_tpl.ttl
./run_xr2rml_annotation.sh $dataset abstract  spotlight_light     xr2rml_spotlight_tpl.ttl

# Generate annotations Entity-fishing
./run_xr2rml_annotation.sh $dataset title     entityfishing_abstract xr2rml_entityfishing_tpl.ttl
./run_xr2rml_annotation.sh $dataset abstract  entityfishing_abstract xr2rml_entityfishing_tpl.ttl
./run_xr2rml_annotation.sh $dataset body_text entityfishing_abody    xr2rml_entityfishing_tpl.ttl
