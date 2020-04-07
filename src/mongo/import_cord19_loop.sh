#!/bin/bash

# CORD19 dataset
VERSION=6
ARCHIVE=$HOME/public_html/CORD-19-V${VERSION}

# MongoDB database
DB=cord19v${VERSION}


# Import all JSON files one by one into MongoDB
#   $1: directory where to find the JSON files
#   $2: prefix of the collection names: prefix_0, prefix_1, ...
import_mongo() {
    DIR=$1
    COLLECTION=$2
    for jsonfile in `ls $DIR/*.json`; do
        echo "Importing file $jsonfile"
        mongoimport --type=json -d $DB -c $COLLECTION $jsonfile
    done
}

# Import all JSON files one by one into MongoDB.
# Same as import_mongo but drops the collection first.
#   $1: directory where to find the JSON files
#   $2: prefix of the collection names: prefix_0, prefix_1, ...
drop_import_mongo() {
    DIR=$1
    COLLECTION=$2
    mongo --eval "db.${COLLECTION}.drop()" localhost/$db

    for jsonfile in `ls $DIR/*.json`; do
        echo "Importing file $jsonfile"
        mongoimport --type=json -d $DB -c $COLLECTION $jsonfile
    done

    mongo --eval "db.${COLLECTION}.createIndex({paper_id: 1})" localhost/$DB
}

# Import JSON files one by one into MongoDB collections with a max number of files per collection
# and create as many collections as needed.
#   $1: directory where to find the JSON files
#   $2: prefix of the collection names: prefix_0, prefix_1, ...
#   $3: max number of files per collection
drop_import_mongo_split(){
    DIR=$1
    COLLECTION=$2
    MAXFILES=$3

    # Get the whole list of files to import into MongoDB
    filelist=/tmp/filelist-$$.txt
    ls -1 $DIR/*.json > $filelist

    # Split the list of files into multiple pieces of $MAXFILES files
    prefix=/tmp/filelist-$$-
    split -d -l $MAXFILES $filelist $prefix
    rm -f $filelist

    # Import the lists of files into separate collections
    colIndex=0
    for filelist in `ls ${prefix}*`; do

        col=${COLLECTION}_${colIndex}
        echo "----- Creating collection $col"
        mongo --eval "db.${col}.drop()" localhost/$db

        # Import each json file in the current collection
        for jsonfile in `cat $filelist`; do
            echo "Importing $jsonfile into collection $col"
            mongoimport --type=json -d $DB -c $col $jsonfile
        done

        mongo --eval "db.${col}.createIndex({paper_id: 1})" localhost/$DB

        # Next collection
        colIndex=$(($colIndex + 1))
    done
}


# Import the original CORD19 corpus
import_cord_metadata() {
    # Metadata of all articles in the CORD19 dataset
    COLLECTION=cord19_metadata
    mongoimport --drop --type=csv --headerline --ignoreBlanks -d $DB -c $COLLECTION $ARCHIVE/metadata_fixed.csv
    mongo --eval "db.${COLLECTION}.createIndex({paper_id: 1})" localhost/$DB
}


# Import the original CORD19 corpus
import_cord_json() {
    # Importing the set of JSON files is not necessary to generate CORD19-NEKG
    COLLECTION=cord19_json
    mongo --eval "db.${COLLECTION}.drop()" localhost/$db

    import_mongo $ARCHIVE/biorxiv_medrxiv     $COLLECTION
    import_mongo $ARCHIVE/comm_use_subset     $COLLECTION
    import_mongo $ARCHIVE/noncomm_use_subset  $COLLECTION
    import_mongo $ARCHIVE/pmc_custom_license  $COLLECTION

    mongo --eval "db.${COLLECTION}.createIndex({paper_id: 1})" localhost/$DB
}


# Import the CORD19 DBpedia-Spotlight annotations
import_spotlight_single() {
    COLLECTION=spotlight
    mongo --eval "db.${COLLECTION}.drop()" localhost/$db

    import_mongo ${ARCHIVE}-Annotation/dbpedia-spotlight/biorxiv_medrxiv/pdf_json    ${COLLECTION}
    import_mongo ${ARCHIVE}-Annotation/dbpedia-spotlight/comm_use_subset/pdf_json    ${COLLECTION}
    import_mongo ${ARCHIVE}-Annotation/dbpedia-spotlight/comm_use_subset/pmc_json    ${COLLECTION}
    import_mongo ${ARCHIVE}-Annotation/dbpedia-spotlight/noncomm_use_subset/pdf_json ${COLLECTION}
    import_mongo ${ARCHIVE}-Annotation/dbpedia-spotlight/noncomm_use_subset/pmc_json ${COLLECTION}
    import_mongo ${ARCHIVE}-Annotation/dbpedia-spotlight/pmc_custom_license/pdf_json ${COLLECTION}
    import_mongo ${ARCHIVE}-Annotation/dbpedia-spotlight/pmc_custom_license/pmc_json ${COLLECTION}

    mongo --eval "db.${COLLECTION}.createIndex({paper_id: 1})" localhost/$DB
}


# Import the CORD19 DBpedia-Spotlight annotations into separate collections
import_spotlight_separate() {
    COLLECTION=spotlight
    drop_import_mongo ${ARCHIVE}-Annotation/dbpedia-spotlight/biorxiv_medrxiv/pdf_json    ${COLLECTION}_biorxiv_medrxiv
    drop_import_mongo ${ARCHIVE}-Annotation/dbpedia-spotlight/comm_use_subset/pdf_json    ${COLLECTION}_comm_use_subset
    drop_import_mongo ${ARCHIVE}-Annotation/dbpedia-spotlight/comm_use_subset/pmc_json    ${COLLECTION}_comm_use_subset
    drop_import_mongo ${ARCHIVE}-Annotation/dbpedia-spotlight/noncomm_use_subset/pdf_json ${COLLECTION}_noncomm_use_subset
    drop_import_mongo ${ARCHIVE}-Annotation/dbpedia-spotlight/noncomm_use_subset/pmc_json ${COLLECTION}_noncomm_use_subset
    drop_import_mongo ${ARCHIVE}-Annotation/dbpedia-spotlight/pmc_custom_license/pdf_json ${COLLECTION}_pmc_custom_license
    drop_import_mongo ${ARCHIVE}-Annotation/dbpedia-spotlight/pmc_custom_license/pmc_json ${COLLECTION}_pmc_custom_license
}


# Import the CORD19 Entity-fishing annotations
import_entityfishing_separate(){
    COLLECTION=entityfishing
    drop_import_mongo ${ARCHIVE}-Annotation/entity-fishing/biorxiv_medrxiv/pdf_json    ${COLLECTION}_biorxiv_medrxiv
    #drop_import_mongo ${ARCHIVE}-Annotation/entity-fishing/comm_use_subset/pdf_json    ${COLLECTION}_comm_use_subset
    #drop_import_mongo ${ARCHIVE}-Annotation/entity-fishing/comm_use_subset/pmc_json    ${COLLECTION}_comm_use_subset
    #drop_import_mongo ${ARCHIVE}-Annotation/entity-fishing/noncomm_use_subset/pdf_json ${COLLECTION}_noncomm_use_subset
    #drop_import_mongo ${ARCHIVE}-Annotation/entity-fishing/noncomm_use_subset/pmc_json ${COLLECTION}_noncomm_use_subset
    #drop_import_mongo ${ARCHIVE}-Annotation/entity-fishing/pmc_custom_license/pdf_json ${COLLECTION}_pmc_custom_license
    #drop_import_mongo ${ARCHIVE}-Annotation/entity-fishing/pmc_custom_license/pmc_json ${COLLECTION}_pmc_custom_license
}

#import_cord_metadata
#import_cord_json
#import_spotlight_separate
import_spotlight_single
import_entityfishing_separate


# -----------------------------------------------------------
# For information - Number of JSON files in the CORD19 v6 dataset
# ll biorxiv_medrxiv/pdf_json/ | wc -l
# ll comm_use_subset/pdf_json/ | wc -l
# ll comm_use_subset/pmc_json/ | wc -l
# ll custom_license/pdf_json/ | wc -l
# ll custom_license/pmc_json/ | wc -l
# ll noncomm_use_subset/pdf_json/| wc -l
# ll noncomm_use_subset/pmc_json/| wc -l
#
# biorxiv_medrxiv/pdf_json      1343
# comm_use_subset/pdf_json      9366
# comm_use_subset/pmc_json      8996
# custom_license/pdf_json       23153
# custom_license/pmc_json       4774
# noncomm_use_subset/pdf_json   2378
# noncomm_use_subset/pmc_json   2094
# -----------------------------------------------------------
