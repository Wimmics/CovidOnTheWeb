This folder provides tools to import three different datasets into MongoDB, that are involved in the the generation the Covid-On-The-Web RDF dataset.

- CORD-19 (metadat.csv + per-article JSON files)
- Named entities computed by DBpedia Spotlight, Entity-fishing and NCBO Bioportal Annotator
- Arguments extracted by the [ACTA](http://ns.inria.fr/acta/) platform.

Script `import-cord19.sh` is the entry point. 
Uncomment the lines at the end of the script as needed to import datasets.
It loads the datasets and creates derived collections using the `*.js` files.

Script `import-tools.sh` defines functions to load groups of JSON files into MongoDB.
These are necessary as CORD-19 (as well as the Entity-fishing, Spotlight and Bioportal Annotator datasets) contains 50,000+ JSON files, possibly large, that cannot be loaded at once into MongoDB. 
Hence the need to split the files into multiple smaller groups.
