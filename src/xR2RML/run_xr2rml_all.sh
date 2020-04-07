#!/bin/bash
# Author: F. Michel, UCA, CNRS, Inria

dataset=dataset-1-0

# Generate articles metadata
./run_xr2rml_metadata.sh   $dataset cord19_csv sha   xr2rml_metadata_sha_tpl.ttl
./run_xr2rml_metadata.sh   $dataset cord19_csv pmcid xr2rml_metadata_pmcid_tpl.ttl


# Generate annotations

./run_xr2rml_annotation.sh $dataset title     spotlight_biorxiv_medrxiv     xr2rml_spotlight_tpl.ttl
./run_xr2rml_annotation.sh $dataset abstract  spotlight_biorxiv_medrxiv     xr2rml_spotlight_tpl.ttl
./run_xr2rml_annotation.sh $dataset body_text spotlight_biorxiv_medrxiv     xr2rml_spotlight_tpl.ttl




