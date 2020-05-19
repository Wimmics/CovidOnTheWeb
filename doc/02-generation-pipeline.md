# Covid-On-The-Web Generation Pipeline

Several steps are involved in the generation the Covid-On-The-Web RDF dataset.

### Articles mining

The processing of the CORD-19 corpus (set of JSON documents) with [DBpedia Spotlight](https://www.dbpedia-spotlight.org/), [entity-fishing](https://github.com/kermitt2/entity-fishing) and [NCBO BioPortal annotator](http://bioportal.bioontology.org/annotatorplus) results in one JSON document per article and per named-entity recognition/disambiguation tool.

Similarly, the processing of the CORD-19 corpus with [ACTA](http://ns.inria.fr/acta/) results in one JSON document per article.


### RDF files generation

The resulting JSON documents are imported into a MongoDB database. Pre-processing is then achieved using MongoDB aggregation queries, such as cleaning authors names and filtering out of named entities that are less than 3 characters long.
The scripts involved at this step are provided in [/src/mongo](../src/mongo).

The RDF files are then generated using [Morph-xR2RML](https://github.com/frmichel/morph-xr2rml/), an implementation of the [xR2RML mapping language](http://i3s.unice.fr/~fmichel/xr2rml_specification.html) [1] for MongoDB databases.
Scripts and mapping files are provided in [/src/xR2RML](../src/xR2RML).

Finally, RDF files are imported into a Virtuoso OS instance as separate named graphs. 
Scripts are provided in [/src/virtuoso](../src/virtuoso).


### Generation of articles metadata RDF files

CORD-19 provides metadata about articles as a large CSV file. Similarly to the above steps, the file was imported into MongoDB and translated to RDF using Morph-xR2RML.
All the scripts involved are available in the folders mentioned above.

### References

[1] F. Michel, L. Djimenou, C. Faron-Zucker, and J. Montagnat. Translation of Relational and Non-Relational Databases into RDF with xR2RML.
In Proceedings of the *11th International Confenrence on Web Information Systems and Technologies (WEBIST 2015)*, Lisbon, Portugal, 2015.

