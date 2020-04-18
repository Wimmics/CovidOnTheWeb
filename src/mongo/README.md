This folder provides tools to import three different datasets into MongoDB:
- CORD-19 (metadat.csv + per-article JSON files)
- Named entities computed by DBpedia Spotlight on CORD-19
- Named entities computed by entity-fishing on CORD-19

Script `import-cord19.sh` is the entry point. 

Uncomment the lines at the end of the script as needed to import datasets.
It loads the datasets and create derived *light* collections using the `lighten_*.js` files.


Script `import-tools.sh` defines functions to load group JSON files into MongoDB.
These are necessary as CORD-19 (as well as the entity-fishing and Spotlight datasets) contains 50,000+ JSON files, possibly large, that cannot be loaded into MongoDB at once. 
Hence the need to split the files into multiple smaller groups.

