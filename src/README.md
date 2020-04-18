# Generation of the CORD19-NEKG dataset

This folder provides the scripts and mappings files needed to translate into RDF the following datasets:
- CORD-19 (metadat.csv + per-article JSON files)
- Named entities computed by DBpedia Spotligt on CORD-19
- Named entities computed by entity-fishing on CORD-19

The following steps are involved in the generation the CORD19-NEKG RDF dataset:
- datasets are loaded into a MongoDB as collections (see [mongo](mongo))
- collections are translated to RDF using Morph-xR2RLM (see [xR2RML](xR2RML))
- the files produced are loaded into a Virtuoso triple store as named graphs (see [virtuoso](virtuoso))

