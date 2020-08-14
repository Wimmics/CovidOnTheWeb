#!/bin/bash
# Query DBpedia for each of the URIs to retrieve the hierarchy of classes of each URI.

# SPARQL query pattern
query_pattern=`cat query-hierarchy.sparql`

# List of URIs to query
urilist=dbpedia-ne-uris.ttl

# Max number of URIs to query at once
MAXURIS=50

# Split the list of URIs into multiple files of $MAXURIS URIs
urilist_split=/tmp/urilist-$$-
split -d -l $MAXURIS $urilist $urilist_split


# Loop on all files of URIs
nbfiles=$(ls -l ${urilist_split}* | wc -l)
nbfiles=$(($nbfiles - 1))
_fileIndex=0
for _uri_file_list in `ls ${urilist_split}*`; do
    echo ""
    echo "--- Processing file $_uri_file_list (${_fileIndex}/$nbfiles)"

    # Create the list of URIs to embed in the SPARQL query
    _uri_list=''
    for _uri in `cat $_uri_file_list`; do
        _uri_list="$_uri_list <${_uri}>"
    done
    # Add commas between URIs: replace each "> <" by ">, <"
    _uri_list="${_uri_list//> </>, <}"

    curl -o dumps/dump_${_fileIndex}.ttl \
         -X POST \
         -H 'Accept: text/turtle' \
         -H "Content-Type: application/sparql-query" \
         -d "${query_pattern/\{\{uri_list\}\}/$_uri_list}" \
         https://dbpedia.org/sparql

    rm -f $_uri_file_list
    _fileIndex=$(($_fileIndex + 1))
done

exit
# -----------------------

# Upload the graph to Virtuoso
DIR=$(pwd)/dumps
graph="http://ns.inria.fr/covid19/graph/dbpedia-named-entities"
../virtuoso/virtuoso-import.sh \
    --cleargraph \
    --graph $graph \
    --path $DIR \
     'dump_*.ttl'
