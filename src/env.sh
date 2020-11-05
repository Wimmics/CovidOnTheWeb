#!/bin/bash
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#
# Tune the variables in this file according to the environment


# Version and release date of the CORD19 dataset being processed
CORD19_VERSION=47
CORD19_DATE=2020-09-01


# Directory of CORD19 archive (unzipped)
CORD19_DIR=/appli/cord19/CORD-19-V${CORD19_VERSION}

# Directory of DBpedia Spotlight annotations (unzipped)
CORD19_SPOTLIGHT=/appli/cord19/CORD-19-V${CORD19_VERSION}-Annotation/dbpedia-spotlight

# Directory of DBpedia Spotlight annotations (unzipped)
CORD19_EF=/appli/cord19/CORD-19-V${CORD19_VERSION}-Annotation/entity-fishing

# Directory of Bioportal Annotator annotations (unzipped)
CORD19_NCBO=/appli/cord19/CORD-19-V${CORD19_VERSION}-Annotation/ncbo

# Directory of ACTA files (unzipped)
CORD19_ACTA=/appli/cord19/CORD-19-V${CORD19_VERSION}-ACTA


# Covid-on-the-Web version (dot- and dashed-notation)
COTW_VERSION=1.2
COTW_VERSION_DASH=1-2

# Covid-on-the-Web dataset id (end of the dataset URI)
COTW_DATASET=dataset-${COTW_VERSION_DASH}


# MongoDB database
DB=cord19v${CORD19_VERSION}
