#!/bin/bash
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria

# CORD19 and Covid-on-the-Web environment definitions
. ../env.sh

# Directory where the output files are stored (relative to the current directory)
ODIR=./$COTW_DATASET
mkdir -p $ODIR


# Generate articles metadata
./run_xr2rml_metadata.sh $COTW_DATASET cord19_metadata sha   xr2rml_metadata_sha_tpl.ttl   $ODIR/cord19-articles-metadata-sha.ttl
./run_xr2rml_metadata.sh $COTW_DATASET cord19_metadata pmcid xr2rml_metadata_pmcid_tpl.ttl $ODIR/cord19-articles-metadata-pmcid.ttl
./run_xr2rml_metadata_authors.sh cord19_json_light  xr2rml_metadata_authors_tpl.ttl        $ODIR/cord19-articles-metadata-authors.ttl


# Generate annotations for DBpedia Spotlight
./run_xr2rml_annotation.sh $COTW_DATASET title    spotlight_abstract xr2rml_spotlight_tpl.ttl $ODIR/cord19-nekg-spotlight-title.ttl
./run_xr2rml_annotation.sh $COTW_DATASET abstract spotlight_abstract xr2rml_spotlight_tpl.ttl $ODIR/cord19-nekg-spotlight-abstract.ttl


# Generate annotations for Entity-fishing (title and abstract)
./run_xr2rml_annotation.sh $COTW_DATASET title    entityfishing_abstract xr2rml_entityfishing_tpl.ttl $ODIR/cord19-nekg-entityfishing-title.ttl
./run_xr2rml_annotation.sh $COTW_DATASET abstract entityfishing_abstract xr2rml_entityfishing_tpl.ttl $ODIR/cord19-nekg-entityfishing-abstract.ttl

# Generate annotations for Entity-fishing (body)
collections=$(mongo $DB --eval "db.getCollectionNames()" | cut -d'"' -f2 | egrep "entityfishing_._body")
index=0
for collection in $collections; do
    echo "Processing collection $collection"
    ./run_xr2rml_annotation_split.sh $COTW_DATASET body_text $collection xr2rml_entityfishing_tpl.ttl 10000000 $ODIR/cord19-nekg-entityfishing-body.ttl.${index}
    index=$(($index + 1))
done


# Generate annotations for NCBO Bioportal Annotator
index=0
collections=$(mongo $DB --eval "db.getCollectionNames()" | cut -d'"' -f2 | grep "ncbo_")
for collection in $collections; do
    echo "Processing collection $collection"
    ./run_xr2rml_annotation.sh $COTW_DATASET title    $collection xr2rml_ncbo.ttl $ODIR/cord19-nekg-ncbo-title.ttl.${index}
    ./run_xr2rml_annotation.sh $COTW_DATASET abstract $collection xr2rml_ncbo.ttl $ODIR/cord19-nekg-ncbo-abstract.ttl.${index}
    index=$(($index + 1))
done


# Generate arguments from ACTA
./run_xr2rml_acta.sh $COTW_DATASET acta_components              xr2rml_acta_tpl.ttl      $ODIR/cord19-akg.ttl
./run_xr2rml_acta.sh $COTW_DATASET acta_components_participants xr2rml_acta_pico_tpl.ttl $ODIR/cord19-akg-participant.ttl
./run_xr2rml_acta.sh $COTW_DATASET acta_components_outcomes     xr2rml_acta_pico_tpl.ttl $ODIR/cord19-akg-outcome.ttl
./run_xr2rml_acta.sh $COTW_DATASET acta_components_intervention xr2rml_acta_pico_tpl.ttl $ODIR/cord19-akg-intervention.ttl
