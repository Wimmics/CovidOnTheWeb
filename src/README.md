# Covid-on-the-Web dataset generation pipeline

Several steps are involved in the generation the Covid-On-The-Web RDF dataset.

This folder provides various tools, scripts and mappings files involved in carrying out these steps.


## Articles mining

Directory [ner](ner) provides the tools required to **extraction named entities from CORD-19** using [DBpedia Spotlight](https://www.dbpedia-spotlight.org/), [Entity-fishing](https://github.com/kermitt2/entity-fishing) and [NCBO BioPortal annotator](http://bioportal.bioontology.org/annotatorplus).

Similarly, directory [acta](acta) provides the tools required to **extract arguments from CORD-19** using [ACTA](http://ns.inria.fr/acta/) 

In both cases, one result JSON file is produced per article from the CORD-19 corpus processed.
Directory [mongo](mongo) provides the scrips used to import these different sets of JSON files into MongoDB, and pre-process them with MongoDB aggregation queries to clean up the data and prepare prepare the JSON format for the next stage.

## CORD-19 loading and pre-processing

In addition to the extraction of named entities and arguments from the CORD-19 corpus, we also need to transform the articles metadata in RDF.

CORD-19 provides metadata about articles as a large CSV file, as well as one JSON file for each article in the corpus.

Directory [mongo](mongo) provides the scrips used to import these CORD-19 CSV and JSON files into MongoDB and pre-process them.


## RDF files generation

The translation in RDF of the three sources (CORD-19, named entities, arguments) is carried out using [Morph-xR2RML](https://github.com/frmichel/morph-xr2rml/), an implementation of the [xR2RML mapping language](http://i3s.unice.fr/~fmichel/xr2rml_specification.html) [1] for MongoDB databases.

The scripts, configuration and mapping files are provided in directory [xR2RML](xR2RML).


## RDF files import into Virtuoso

RDF files generated at the previous stage are imported into a Virtuoso OS instance as separate named graphs. 
Scripts are provided in directory [virtuoso](virtuoso).


## References

[1] F. Michel, L. Djimenou, C. Faron-Zucker, and J. Montagnat. Translation of Relational and Non-Relational Databases into RDF with xR2RML.
In Proceedings of the *11th International Confenrence on Web Information Systems and Technologies (WEBIST 2015)*, Lisbon, Portugal, 2015.

