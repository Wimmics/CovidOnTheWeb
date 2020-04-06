#!/bin/bash

VERSION=6
DB=cord19v${VERSION}
ARCHIVE=$HOME/public_html/CORD-19-V${VERSION}

import_cord(){
  COLLECTION=cord19_v${VERSION}_csv
  mongoimport --drop --type=csv --headerline --ignoreBlanks -d $DB -c $COLLECTION ${ARCHIVE}/metadata_fixed.csv


  COLLECTION=cord19_v${VERSION}_json

  cat ${ARCHIVE}/biorxiv_medrxiv/*.json > ${ARCHIVE}/biorxiv_medrxiv.json
  mongoimport --drop --type=json -d $DB -c $COLLECTION ${ARCHIVE}/biorxiv_medrxiv.json
  rm ${ARCHIVE}/biorxiv_medrxiv.json

  cat ${ARCHIVE}/comm_use_subset/*.json > ${ARCHIVE}/comm_use_subset.json
  mongoimport --drop --type=json -d $DB -c $COLLECTION ${ARCHIVE}/comm_use_subset.json
  rm ${ARCHIVE}/comm_use_subset.json

  cat ${ARCHIVE}/noncomm_use_subset/*.json > ${ARCHIVE}/noncomm_use_subset.json
  mongoimport --drop --type=json -d $DB -c $COLLECTION  ${ARCHIVE}/noncomm_use_subset.json
  rm ${ARCHIVE}/noncomm_use_subset.json

  cat ${ARCHIVE}/pmc_custom_license/*.json > ${ARCHIVE}/pmc_custom_license.json
  mongoimport --drop --type=json -d $DB -c $COLLECTION ${ARCHIVE}/pmc_custom_license.json
  rm ${ARCHIVE}/pmc_custom_license.json

  mongo --eval "db.${COLLECTION}.createIndex({paper_id: 1})" localhost/$DB
}

import_spotlight(){
  COLLECTION=spotlight_v${VERSION}

  cat ${ARCHIVE}-Annotation/biorxiv_medrxiv/dbpedia-spotlight/*.json > ${ARCHIVE}-Annotation/biorxiv_medrxiv_spotlight.json
  mongoimport --drop --type=json -d $DB -c $COLLECTION ${ARCHIVE}-Annotation/biorxiv_medrxiv_spotlight.json
  rm ${ARCHIVE}-Annotation/biorxiv_medrxiv_spotlight.json

  cat ${ARCHIVE}-Annotation/comm_use_subset/dbpedia-spotlight/*.json > ${ARCHIVE}-Annotation/comm_use_subset_spotlight.json
  mongoimport --drop --type=json -d $DB -c $COLLECTION ${ARCHIVE}-Annotation/comm_use_subset_spotlight.json
  rm ${ARCHIVE}-Annotation/comm_use_subset_spotlight.json

  cat ${ARCHIVE}-Annotation/noncomm_use_subset/dbpedia-spotlight/*.json > ${ARCHIVE}-Annotation/noncomm_use_subset_spotlight.json
  mongoimport --drop --type=json -d $DB -c $COLLECTION ${ARCHIVE}-Annotation/noncomm_use_subset_spotlight.json
  rm ${ARCHIVE}-Annotation/noncomm_use_subset_spotlight.json

  cat ${ARCHIVE}-Annotation/pmc_custom_license/dbpedia-spotlight/*.json > ${ARCHIVE}-Annotation/pmc_custom_license_spotlight.json
  mongoimport --drop --type=json -d $DB -c $COLLECTION ${ARCHIVE}-Annotation/pmc_custom_license_spotlight.json
  rm ${ARCHIVE}-Annotation/pmc_custom_license_spotlight.json

  mongo --eval "db.${COLLECTION}.createIndex({paper_id: 1})" localhost/$DB
}

import_entityfishing(){
  COLLECTION=entityfishing_v${VERSION}

  cat ${ARCHIVE}-Annotation/biorxiv_medrxiv/entity-fishing/*.json > ${ARCHIVE}-Annotation/biorxiv_medrxiv_fishing.json
  mongoimport --drop --type=json -d $DB -c $COLLECTION ${ARCHIVE}-Annotation/biorxiv_medrxiv_fishing.json
  rm ${ARCHIVE}-Annotation/biorxiv_medrxiv_fishing.json

  cat ${ARCHIVE}-Annotation/comm_use_subset/entity-fishing/*.json > ${ARCHIVE}-Annotation/comm_use_subset_fishing.json
  mongoimport --drop --type=json -d $DB -c $COLLECTION ${ARCHIVE}-Annotation/comm_use_subset_fishing.json
  rm ${ARCHIVE}-Annotation/comm_use_subset_spotlight.json

  cat ${ARCHIVE}-Annotation/noncomm_use_subset/entity-fishing/*.json > ${ARCHIVE}-Annotation/noncomm_use_subset_fishing.json
  mongoimport --drop --type=json -d $DB -c $COLLECTION ${ARCHIVE}-Annotation/comm_use_subset_fishing.json
  rm ${ARCHIVE}-Annotation/comm_use_subset_fishing.json

  cat ${ARCHIVE}-Annotation/pmc_custom_license/entity-fishing/*.json > ${ARCHIVE}-Annotation/pmc_custom_license_fishing.json
  mongoimport --drop --type=json -d $DB -c $COLLECTION ${ARCHIVE}-Annotation/pmc_custom_license_fishing.json
  rm ${ARCHIVE}-Annotation/pmc_custom_license_fishing.json

  mongo --eval "db.${COLLECTION}.createIndex({paper_id: 1})" localhost/$DB
}

import_cord
import_spotlight
import_entityfishing
