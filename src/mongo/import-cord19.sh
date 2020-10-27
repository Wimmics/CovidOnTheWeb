#!/bin/bash
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)


# Functions definitions
. ./import-tools.sh

# CORD19 dataset
VERSION=47
ARCHIVE=/appli/cord19/CORD-19-V${VERSION}

# MongoDB database
DB=cord19v${VERSION}


# ------------------------------------------------------------------------------

# Import the CORD19 metadata (metadata.csv)
import_cord_metadata() {
    # Metadata of all articles in the CORD19 dataset
    collection=cord19_metadata
    mongoimport --drop --type=csv --headerline --ignoreBlanks -d $DB -c $collection $ARCHIVE/metadata_fixed.csv
    mongo --eval "db.${collection}.createIndex({paper_id: 1})" localhost/$DB
}


# Import the CORD19 JSON files
import_cord_json() {
    collection=cord19_json
    mongo_drop_import_dir ${ARCHIVE} ${collection}

    # Create collection cord19_json_light
    mongo localhost/$DB lighten_cord19json.js
}

# ------------------------------------------------------------------------------

# Import CORD19 DBpedia-Spotlight annotations in a single collection
import_spotlight_single() {
    collection=spotlight
    mongo_drop_import_dir ${ARCHIVE}-Annotation/dbpedia-spotlight ${collection}

    # Create collection spotlight_light
    mongo localhost/$DB lighten_spotlight.js
}


# Import CORD19 Entity-fishing annotations in a single collection
import_entityfishing_single() {
    collection=entityfishing
    mongo_drop_import_dir ${ARCHIVE}-Annotation/entity-fishing ${collection}

    # Create lightened collection
    mongo localhost/$DB lighten_entityfishing_abstract.js
}


# Import CORD19 Entity-fishing annotations in a multiple collections
import_entityfishing_multiple() {
    collection=entityfishing
    mongo_drop_import_dir_split ${ARCHIVE}-Annotation/entity-fishing ${collection} 30000

    # List the imported collections
    collections=$(mongo --eval "db.getCollectionNames()" cord19v47 | sed 's|[",[:space:]]||g' | egrep "entityfishing_[[:digit:]]+")

    # Create lightened collection for each imported collection
    for collection in $collections; do
        echo "----- Lightening collection $collection"
        sed "s|COLLECTION|$collection|g" lighten_entityfishing_body.js > lighten_entityfishing_body_tmp.js
        mongo localhost/$DB lighten_entityfishing_body_tmp.js
    done
    rm -f lighten_entityfishing_body_tmp.js
}


# Import CORD19 NCBO Annotator annotations in a multiple collections
import_ncbo() {
    collection=ncbo
    mongo_drop_import_dir_split ${ARCHIVE}-Annotation/ncbo-light ${collection} 5000
}

# ------------------------------------------------------------------------------

# Import CORD19 ACTA annotations in a multiple collection
import_acta() {
    collection=acta
    mongo_drop_import_dir ${ARCHIVE}-ACTA ${collection}

    # Create collection acta_claim & acta_evid
    mongo localhost/$DB filter-acta.js
}

# ------------------------------------------------------------------------------

# -- Uncomment the following lines as needed to import datasets --

#import_cord_metadata
#import_cord_json
#import_entityfishing_single
#import_entityfishing_multiple
#import_spotlight_single
#import_ncbo
#import_acta



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
