#!/bin/bash

# In case there are multiple sha values in the paper_id ("sha1; sha2; sha3..."), only keep the first one
sed -r 's|,([a-f0-9]+)(; [a-f0-9]+)+|,\1|g' metadata.csv > _tmp_metadata.csv

# Paper 6ef30c327132cbdcf5ee67605fa41086ef43fed4 has a wrong doi containing '<' and '>' characters.
# Can't be used to create an IRI => simply remove it
grep -v 6ef30c327132cbdcf5ee67605fa41086ef43fed4 _tmp_metadata.csv > metadata_fixed.csv

rm -f _tmp_metadata.csv
