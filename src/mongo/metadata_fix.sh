#!/bin/bash

# In case there are multiple sha values in the paper_id ("sha1; sha2; sha3..."), only keep the first one
sed -r 's|,([a-f0-9]+)(; [a-f0-9]+)+|,\1|g' metadata.csv > metadata_fixed.csv

rm -f _tmp_metadata.csv
