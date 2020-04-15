#!/bin/bash

# CORD19 dataset
VERSION=7
ARCHIVE=$HOME/public_html/CORD-19-V${VERSION}

# MongoDB database
DB=cord19v${VERSION}

# Max number of files to import at once into MongoDB
MONGO_IMPORT_MAXFILE=1000


# Import, into a MongoDB collection, the JSON files listed in a file.
# Files are imported by groups of a max number of files.
#   $1: MongoDB collection name
#   $2: file containing the list of JSON files to import
#   $3: max number of files to import at once
mongo_import_filelist() {
    _collection_a=$1
    _filelist_a=$2
    _maxfiles_a=$3
    
    # Split the list of files into multiple pieces of $_maxfiles files
    _prefix_a=/tmp/filelist-$$-
    split -d -l $_maxfiles_a $_filelist_a $_prefix_a
    
    # Import the files by groups
    jsondump=jsondump-$$
    for _filelist_a in `ls ${_prefix_a}*`; do
        echo -n '' > $jsondump
        
        for jsonfile in `cat $_filelist_a`; do
            echo "Importing document $jsonfile"
            cat $jsonfile >> $jsondump
        done
        echo "Importing documents from $jsondump"
        mongoimport --type=json -d $DB -c $_collection_a $jsondump
    done
    
    rm -f $jsondump ${_prefix_a}*    
}


# Import, into a MongoDB collection, all JSON files of a directory including sub-directories
#   $1: directory where to find the JSON files
#   $2: MongoDB collection name
mongo_import_dir() {
    _dir_b=$1
    _collection_b=$2

    # Get the list of files to import into MongoDB
    _filelist_b=/tmp/filelist-$$.txt
    find $_dir_b -type f -name '*.json' > $_filelist_b

    mongo_import_filelist $_collection_b $_filelist_b $MONGO_IMPORT_MAXFILE
    rm -f $_filelist_b
}


# Import, into a MongoDB collection, all JSON files of a directory including sub-directories
# Same as mongo_import_dir but first drops the collection and creates an index afterwards.
#   $1: directory where to find the JSON files
#   $2: MongoDB collection name
mongo_drop_import_dir() {
    _collection_c=$2
    mongo --eval "db.${_collection_c}.drop()" localhost/$DB
    mongo_import_dir $1 $_collection_c
    mongo --eval "db.${_collection_c}.createIndex({paper_id: 1})" localhost/$DB
}


# Import all JSON files of a directory into multiple MongoDB collections of a maximum number of files each.
#   $1: directory where to find the JSON files
#   $2: prefix of the collection names: prefix_0, prefix_1, ...
#   $3: max number of files per collection
mongo_drop_import_dir_split(){
    _dir_c=$1
    _collection_c=$2
    _maxfilesPerCollection=$3

    # Get the whole list of files to import into MongoDB
    _filelist_c=/tmp/filelist-collection-$$.txt
    find $_dir_c -type f -name '*.json' > $_filelist_c

    # Split the list of files into multiple pieces of $_maxfilesPerCollection files
    _prefix_c=/tmp/filelist-collection-$$-
    split -d -l $_maxfilesPerCollection $_filelist_c $_prefix_c
    rm -f $_filelist_c

    # Import the lists of files into separate collections
    colIndex=0
    for _filelist_c in `ls ${_prefix_c}*`; do

        col=${_collection_c}_${colIndex}
        echo "----- Creating collection $col"
        mongo_import_filelist $col $_filelist_c $MONGO_IMPORT_MAXFILE

        # Next collection
        colIndex=$(($colIndex + 1))
    done
    rm -f ${_prefix_c}*
}


# ------------------------------------------------------------------------------


# Import the CORD19 metadata (metadata.csv)
import_cord_metadata() {
    # Metadata of all articles in the CORD19 dataset
    collection=cord19_metadata
    mongoimport --drop --type=csv --headerline --ignoreBlanks -d $DB -c $collection $ARCHIVE/metadata_fixed.csv
    mongo --eval "db.${collection}.createIndex({paper_id: 1})" localhost/$DB
}


# Import the CORD19 JSON files
# Note: not necessary to generate CORD19-NEKG
import_cord_json() {
    collection=cord19_json
    mongo_drop_import_dir ${ARCHIVE} ${collection}
}


# Import the CORD19 DBpedia-Spotlight annotations
import_spotlight_single() {
    collection=spotlight
    mongo_drop_import_dir ${ARCHIVE}-Annotation/dbpedia-spotlight ${collection}
}


# Import the CORD19 DBpedia-Spotlight annotations into separate collections
import_spotlight_separate() {
    collection=spotlight
    mongo_drop_import_dir ${ARCHIVE}-Annotation/dbpedia-spotlight/biorxiv_medrxiv    ${collection}_biorxiv_medrxiv
    mongo_drop_import_dir ${ARCHIVE}-Annotation/dbpedia-spotlight/comm_use_subset    ${collection}_comm_use_subset
    mongo_drop_import_dir ${ARCHIVE}-Annotation/dbpedia-spotlight/custom_license     ${collection}_custom_license
    mongo_drop_import_dir ${ARCHIVE}-Annotation/dbpedia-spotlight/noncomm_use_subset ${collection}_noncomm_use_subset
}


# Import the CORD19 Entity-fishing annotations
import_entityfishing_single() {
    collection=entityfishing
    mongo_drop_import_dir ${ARCHIVE}-Annotation/entity-fishing ${collection}
}


# Import the CORD19 Entity-fishing annotations into separate collections
import_entityfishing_separate(){
    collection=entityfishing
    mongo_drop_import_dir ${ARCHIVE}-Annotation/entity-fishing/biorxiv_medrxiv    ${collection}_biorxiv_medrxiv
    mongo_drop_import_dir ${ARCHIVE}-Annotation/entity-fishing/comm_use_subset    ${collection}_comm_use_subset
    mongo_drop_import_dir ${ARCHIVE}-Annotation/entity-fishing/custom_license     ${collection}_custom_license
    mongo_drop_import_dir ${ARCHIVE}-Annotation/entity-fishing/noncomm_use_subset ${collection}_noncomm_use_subset
}

#import_cord_metadata
#import_cord_json
#import_spotlight_separate
#import_spotlight_single
#import_entityfishing_separate
#import_entityfishing_single


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
# ==> 52097
# -----------------------------------------------------------
