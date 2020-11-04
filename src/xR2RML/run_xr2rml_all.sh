#!/bin/bash
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria

# CORD19 version
VERSION=47
DB=cord19v${VERSION}

# Dataset id (part of the dataset URI)
dataset=dataset-1-2


# Generate articles metadata
./run_xr2rml_metadata.sh         $dataset cord19_metadata sha   xr2rml_metadata_sha_tpl.ttl
./run_xr2rml_metadata.sh         $dataset cord19_metadata pmcid xr2rml_metadata_pmcid_tpl.ttl
./run_xr2rml_metadata_authors.sh cord19_json_light     xr2rml_metadata_authors_tpl.ttl


# Generate annotations for DBpedia Spotlight
./run_xr2rml_annotation.sh       $dataset title     spotlight_abstract     xr2rml_spotlight_tpl.ttl
./run_xr2rml_annotation.sh       $dataset abstract  spotlight_abstract     xr2rml_spotlight_tpl.ttl


# Generate annotations for Entity-fishing (title and abstract)
./run_xr2rml_annotation.sh       $dataset title     entityfishing_abstract xr2rml_entityfishing_tpl.ttl
./run_xr2rml_annotation.sh       $dataset abstract  entityfishing_abstract xr2rml_entityfishing_tpl.ttl

# Generate annotations for Entity-fishing (body)
collections=$(mongo $DB --eval "db.getCollectionNames()" | cut -d'"' -f2 | egrep "entityfishing_._body")
for collection in $collections; do
    echo "Processing collection $collection"
    ./run_xr2rml_annotation_split.sh  $dataset  body_text  $collection  xr2rml_entityfishing_tpl.ttl 10000000
done


# Generate annotations for NCBO Bioportal Annotator
collections=$(mongo $DB --eval "db.getCollectionNames()" | cut -d'"' -f2 | grep "ncbo_")
for collection in $collections; do
    echo "Processing collection $collection"
    ./run_xr2rml_annotation.sh  $dataset  title     $collection  xr2rml_ncbo.ttl
    #./run_xr2rml_annotation.sh  $dataset  abstract  $collection  xr2rml_ncbo.ttl
done


# Generate arguments from ACTA
./run_xr2rml_acta.sh  $dataset  acta_components               xr2rml_acta_tpl.ttl
./run_xr2rml_acta.sh  $dataset  acta_components_participants  xr2rml_acta_pico_tpl.ttl
./run_xr2rml_acta.sh  $dataset  acta_components_outcomes      xr2rml_acta_pico_tpl.ttl
./run_xr2rml_acta.sh  $dataset  acta_components_intervention  xr2rml_acta_pico_tpl.ttl
