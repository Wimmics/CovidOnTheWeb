#!/bin/bash
#
# WARNING - Run the commands below from directory 'virtuoso'

# CORD19 and Covid-on-the-Web environment definitions
. ../env.sh

CURRENT_DIR=$(pwd)

# Directory where the ttl files are stored
DATASET_DIR=$CURRENT_DIR/../xR2RML/$COTW_DATASET


# Metadata graph
graph="http://ns.inria.fr/covid19/graph/metadata"
./virtuoso-import.sh \
    --cleargraph \
    --graph $graph \
    --path $CURRENT_DIR/../dataset_tpl \
    covidontheweb-metadata-dataset.ttl covidontheweb-definitions.ttl


# Articles metadata graph - generated from the CORD19 metadata.csv and json files
graph="http://ns.inria.fr/covid19/graph/articles"
./virtuoso-import.sh \
    --cleargraph \
    --graph $graph \
    --path $DATASET_DIR \
    cord19-articles-metadata-authors.ttl cord19-articles-metadata-pmcid.ttl cord19-articles-metadata-sha.ttl


# Entity-fishing graph - article titles and abstracts
graph="http://ns.inria.fr/covid19/graph/entityfishing"
./virtuoso-import.sh \
    --cleargraph \
    --graph $graph \
    --path $DATASET_DIR \
    cord19-nekg-entityfishing-title.ttl cord19-nekg-entityfishing-abstract.ttl


# Entity-fishing graph - articles bodies
graph="http://ns.inria.fr/covid19/graph/entityfishing/body"
./virtuoso-import.sh \
    --cleargraph \
    --graph $graph \
    --path $DATASET_DIR \
    'cord19-nekg-entityfishing-body.ttl.*'


# DBpedia Spotlight graph
graph="http://ns.inria.fr/covid19/graph/dbpedia-spotlight"
./virtuoso-import.sh \
    --cleargraph \
    --graph $graph \
    --path $DATASET_DIR \
    cord19-nekg-spotlight-title.ttl cord19-nekg-spotlight-abstract.ttl


# Bioportal Annotator graph
graph="http://ns.inria.fr/covid19/graph/bioportal-annotator"
./virtuoso-import.sh \
    --cleargraph \
    --graph $graph \
    --path $DATASET_DIR \
    'cord19-nekg-ncbo-title.ttl.*' 'cord19-nekg-ncbo-abstract.ttl.*'


# ACTA graph
graph="http://ns.inria.fr/covid19/graph/acta"
./virtuoso-import.sh \
    --cleargraph \
    --graph $graph \
    --path $DATASET_DIR \
    cord19-akg.ttl cord19-akg-outcome.ttl cord19-akg-intervention.ttl cord19-akg-participant.ttl
