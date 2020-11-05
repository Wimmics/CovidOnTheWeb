#!/bin/bash

# CORD19 and Covid-on-the-Web environment definitions
. ../env.sh

# Directory where the ttl files are stored (relative to the current directory)
DATASET_DIR=./$COTW_DATASET

mkdir -p $DATASET_DIR


# Articles metadata
mv output_cord19_json_light_authors.ttl          $DATASET_DIR/cord19-articles-metadata-authors.ttl
mv output_cord19_metadata_pmcid.ttl              $DATASET_DIR/cord19-articles-metadata-pmcid.ttl
mv output_cord19_metadata_sha.ttl                $DATASET_DIR/cord19-articles-metadata-sha.ttl

# DBpedia Spotlight
mv output_spotlight_abstract_title.ttl           $DATASET_DIR/cord19-nekg-spotlight-title.ttl
mv output_spotlight_abstract_abstract.ttl        $DATASET_DIR/cord19-nekg-spotlight-abstract.ttl

# Entity-fishing
mv output_entityfishing_abstract_title.ttl       $DATASET_DIR/cord19-nekg-entityfishing-title.ttl
mv output_entityfishing_abstract_abstract.ttl    $DATASET_DIR/cord19-nekg-entityfishing-abstract.ttl

# Entity-fishing body annotations
index=0
for file in `ls output_entityfishing_*_body_body_text.ttl.*`; do
    mv $file $DATASET_DIR/cord19-nekg-entityfishing-body.ttl.${index}
    index=$(($index + 1))
done

# NCBO annotations
index=0
for file in `ls output_ncbo_*_title.ttl`; do
    mv $file $DATASET_DIR/cord19-nekg-ncbo-title.ttl.${index}
    index=$(($index + 1))
done
index=0
for file in `ls output_ncbo_*_abstract.ttl`; do
    mv $file $DATASET_DIR/cord19-nekg-ncbo-abstract.ttl.${index}
    index=$(($index + 1))
done

# ACTA
mv output_acta_components.ttl               $DATASET_DIR/cord19-akg.ttl
mv output_acta_components_outcomes.ttl      $DATASET_DIR/cord19-akg-outcome.ttl
mv output_acta_components_intervention.ttl  $DATASET_DIR/cord19-akg-intervention.ttl
mv output_acta_components_participants.ttl  $DATASET_DIR/cord19-akg-participant.ttl

