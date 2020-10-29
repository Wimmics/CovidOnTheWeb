#!/bin/bash
# Query Wikidata to retrieve the hierarchy of classes of each URI in file wikidata-ne-uris.txt

# List of URIs to query
urilist=wikidata-ne-uris.txt

# Max number of URIs to query at once
MAXURIS=10

# Initialize the result file with the prefixes
result_file=dump.ttl
cp namespaces.ttl $result_file
result_tmp=/tmp/sparql-response-$$.ttl

# SPARQL query pattern
fullquery_pattern=`cat query-hierarchy.sparql`

# SPARQL parttern for one URI
subquery_pattern='
  { BIND(iri("{{uri}}") as ?uri)
    {?uri wdt:P279+ ?uriParent.}
    UNION
    {?uri wdt:P31/wdt:P279* ?uriClass.}
    UNION
    {?uri wdt:P171* ?uriParent.}
  }
'

# Split the list of URIs into multiple files of $MAXURIS URIs
uri_split=/tmp/uri_list-$$-
split -d -l $MAXURIS $urilist $uri_split

# Loop on all files of URIs
nbfiles=$(ls -l ${uri_split}* | wc -l)
nbfiles=$(($nbfiles - 1))
_fileIndex=0
for _uri_file_list in `ls ${uri_split}*`; do
    echo "--- Processing file $_uri_file_list (${_fileIndex}/$nbfiles)"

    # Create the pattern of the SPARQL query by adding one 
    _subquery='  {}'
    for _uri in `cat $_uri_file_list`; do
        # Add the subquery once for each URI
        _subquery="$_subquery UNION ${subquery_pattern/\{\{uri\}\}/$_uri}"
    done
    rm -f $_uri_file_list
    _fileIndex=$(($_fileIndex + 1))

    curl -o $result_tmp \
         -X POST \
         -H 'Accept: text/turtle' \
         -H "Content-Type: application/sparql-query" \
         -d "${fullquery_pattern/\{\{pattern\}\}/$_subquery}" \
         https://query.wikidata.org/sparql

    # Filter out "@prefix" lines
    cat $result_tmp | grep -v '^@' >> $result_file
    echo "# -----" >> $result_file
done
rm -f $result_tmp

# -----------------------

# Upload the graph to Virtuoso
#CURRENT_DIR=$(pwd)
#graph="http://ns.inria.fr/covid19/graph/wikidata-named-entities-full"
#../virtuoso/virtuoso-import.sh \
#    --cleargraph \
#    --graph $graph \
#    --path $CURRENT_DIR \
#    $result_file
