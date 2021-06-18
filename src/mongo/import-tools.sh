#!/bin/bash
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
#
# Variable $DB must be defined when calling functions of this file.

# Max sie of JSON files to import at once into MongoDB (16MB)
MONGO_IMPORT_MAXSIZE=16000000


# Import, into a MongoDB collection, the JSON files listed in a file.
# Files are imported one by one.
#   $1: MongoDB collection name
#   $2: file containing the list of JSON files to import
mongo_import_filelist_onebyone() {
    _collection_a=$1
    _filelist_a=$2
    index=0

    for jsonfile in `cat $_filelist_a`; do
    
        filesize=$(stat --format=%s $jsonfile)
        if [ $filesize -ge $MONGO_IMPORT_MAXSIZE ]; then
            echo "WARNING - Ignoring oversized document $jsonfile ($filesize bytes)"
        else
            echo "Importing file $index: $jsonfile"
            mongoimport --type=json -d $DB -c $_collection_a $jsonfile
        fi
        index=$(($index + 1))
    done
}


# Import, into a MongoDB collection, the JSON files listed in a file.
# Files are grouped until a max size limit (see $MONGO_IMPORT_MAXSIZE)
#   $1: MongoDB collection name
#   $2: file containing the list of JSON files to import
mongo_import_filelist() {
    _collection_a=$1
    _filelist_a=$2
    
    # Import the files by groups
    jsondump=jsondump-$$
    echo -n '' > $jsondump

    for jsonfile in `cat $_filelist_a`; do
    
        filesize=$(stat --format=%s $jsonfile)
        if [ $filesize -ge $MONGO_IMPORT_MAXSIZE ]; then
            echo "WARNING - Ignoring oversized document $jsonfile ($filesize bytes)"
        else
            currentsize=$(stat --format=%s $jsondump)
            newsize=$(($currentsize + $filesize))
            if [ $newsize -lt $MONGO_IMPORT_MAXSIZE ]; then
                echo "Appending to $jsondump document $jsonfile"
                cat $jsonfile >> $jsondump
            else
                echo "Importing documents from $jsondump"
                mongoimport --type=json -d $DB -c $_collection_a $jsondump
                echo -n '' > $jsondump
            fi
        fi
    done
    
    # Import the last group that could be less than $MONGO_IMPORT_MAXSIZE
    if [ -s $jsondump ]; then 
    echo "Importing last documents from $jsondump"
        mongoimport --type=json -d $DB -c $_collection_a $jsondump
        echo -n '' > $jsondump
    fi
    
    rm -f $jsondump
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
    echo "Importing $(wc -l $_filelist_b | cut -d' ' -f1) files..."

    mongo_import_filelist $_collection_b $_filelist_b
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
mongo_drop_import_dir_split() {
    _dir_c=$1
    _collection_c=$2
    _maxfilesPerCollection=$3

    # Get the whole list of files to import into MongoDB
    _filelist_c=/tmp/filelist-collection-$$.txt
    find $_dir_c -type f -name '*.json' > $_filelist_c
    echo "Importing $(wc -l $_filelist_c | cut -d' ' -f1) files..."

    # Split the list of files into multiple pieces of $_maxfilesPerCollection files
    _prefix_c=/tmp/filelist-collection-$$-
    split -d -l $_maxfilesPerCollection $_filelist_c $_prefix_c
    rm -f $_filelist_c

    # Import the lists of files into separate collections
    colIndex=0
    for _filelist_c in `ls ${_prefix_c}*`; do

        col=${_collection_c}_${colIndex}
        echo "----- Creating collection $col"
        mongo --eval "db.${col}.drop()" localhost/$DB
        mongo_import_filelist $col $_filelist_c

        # Next collection
        colIndex=$(($colIndex + 1))
    done
    rm -f ${_prefix_c}*
}
