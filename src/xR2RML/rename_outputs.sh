#!/bin/bash

DIR=cord19-nekg-dataset-1.1

# Articles metadata
mv output_cord19_json_light_authors.ttl          $DIR/cord19-nekg-articles-metadata-authors.ttl
mv output_cord19_metadata_pmcid.ttl              $DIR/cord19-nekg-articles-metadata-pmcid.ttl
mv output_cord19_metadata_sha.ttl                $DIR/cord19-nekg-articles-metadata-sha.ttl

# DBpedia Spotlight
mv output_spotlight_abstract_title.ttl           $DIR/cord19-nekg-spotlight-title.ttl
mv output_spotlight_abstract_abstract.ttl        $DIR/cord19-nekg-spotlight-abstract.ttl

# Entity-fishing
mv output_entityfishing_abstract_title.ttl       $DIR/cord19-nekg-entityfishing-title.ttl
mv output_entityfishing_abstract_abstract.ttl    $DIR/cord19-nekg-entityfishing-abstract.ttl

# Entity-fishing body annotations
mv output_entityfishing_body_body_text_categ.ttl $DIR/cord19-nekg-entityfishing-body-categ.ttl
index=0
for file in `ls output_entityfishing_body_body_text.ttl.*`; do
    mv $file $DIR/cord19-nekg-entityfishing-body-ann-sel.ttl.${index}
    index=$(($index + 1))
done
index=0
for file in `ls output_entityfishing_body_body_text_target.ttl.*`; do
    mv $file $DIR/cord19-nekg-entityfishing-body-target.ttl.${index}
    index=$(($index + 1))
done

# NCBO annotations
mv output_ncbo_title.ttl       $DIR/cord19-nekg-ncbo-title.ttl
index=0
for file in `ls output_ncbo_*_abstract.ttl`; do
    mv $file $DIR/cord19-nekg-ncbo-abstract.ttl.${index}
    index=$(($index + 1))
done
