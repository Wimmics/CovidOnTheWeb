#!/bin/bash
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria

# CORD19 and Covid-on-the-Web environment definitions
. ../env.sh


# Generate articles metadata
./run_xr2rml_metadata.sh         $COTW_DATASET cord19_metadata sha   xr2rml_metadata_sha_tpl.ttl
./run_xr2rml_metadata.sh         $COTW_DATASET cord19_metadata pmcid xr2rml_metadata_pmcid_tpl.ttl
./run_xr2rml_metadata_authors.sh cord19_json_light  xr2rml_metadata_authors_tpl.ttl


# Generate annotations for DBpedia Spotlight
./run_xr2rml_annotation.sh       $COTW_DATASET title     spotlight_abstract     xr2rml_spotlight_tpl.ttl
./run_xr2rml_annotation.sh       $COTW_DATASET abstract  spotlight_abstract     xr2rml_spotlight_tpl.ttl


# Generate annotations for Entity-fishing (title and abstract)
./run_xr2rml_annotation.sh       $COTW_DATASET title     entityfishing_abstract xr2rml_entityfishing_tpl.ttl
./run_xr2rml_annotation.sh       $COTW_DATASET abstract  entityfishing_abstract xr2rml_entityfishing_tpl.ttl

# Generate annotations for Entity-fishing (body)
collections=$(mongo $DB --eval "db.getCollectionNames()" | cut -d'"' -f2 | egrep "entityfishing_._body")
for collection in $collections; do
    echo "Processing collection $collection"
    ./run_xr2rml_annotation_split.sh  $COTW_DATASET  body_text  $collection  xr2rml_entityfishing_tpl.ttl 10000000
done


# Generate annotations for NCBO Bioportal Annotator
collections=$(mongo $DB --eval "db.getCollectionNames()" | cut -d'"' -f2 | grep "ncbo_")
for collection in $collections; do
    echo "Processing collection $collection"
    ./run_xr2rml_annotation.sh  $COTW_DATASET  title     $collection  xr2rml_ncbo.ttl
    ./run_xr2rml_annotation.sh  $COTW_DATASET  abstract  $collection  xr2rml_ncbo.ttl
done


# Generate arguments from ACTA
./run_xr2rml_acta.sh  $COTW_DATASET  acta_components               xr2rml_acta_tpl.ttl
./run_xr2rml_acta.sh  $COTW_DATASET  acta_components_participants  xr2rml_acta_pico_tpl.ttl
./run_xr2rml_acta.sh  $COTW_DATASET  acta_components_outcomes      xr2rml_acta_pico_tpl.ttl
./run_xr2rml_acta.sh  $COTW_DATASET  acta_components_intervention  xr2rml_acta_pico_tpl.ttl
