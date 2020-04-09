# CORD-19 Named Entities Knowlegde Graph (CORD19-NEKG)

CORD-19 Named Entities Knowlegde Graph (CORD19-NEKG) is an RDF dataset describing named entities identified in the scholarly articles of the [COVID-19 Open Research Dataset (CORD-19)](https://pages.semanticscholar.org/coronavirus-research), a resource of over 47,000 articles about COVID-19 and the coronavirus family of viruses.

CORD19-NEKG is an initiative of the [Wimmics team](https://team.inria.fr/wimmics/), [I3S laboratory](http://www.i3s.unice.fr/), Université Côte d'Azur, CNRS, Inria.

#### Documentation

- [Data Modeling](/doc/01-data-modeling.md)
- [Generation Pipeline](/doc/02-generation-pipeline.md)


## Named Entities

To identify and disambiguate named entities, we used [DBpedia Spotlight](https://www.dbpedia-spotlight.org/) (links to DBpedia), [entity-fishing](https://github.com/kermitt2/entity-fishing) (links to Wikidata), and [NCBO BioPortal annotator](http://bioportal.bioontology.org/annotatorplus) (links to ontologies in Bioportal).

CORD19-NEKG **v1.0** is based on [CORD-19 v6](https://www.kaggle.com/dataset/08dd9ead3afd4f61ef246bfd6aee098765a19d9f6dbf514f0142965748be859b/version/6). It provides named entities identified by DBpedia Spotlight and entity-fishing in articles titles and abstracts, and only named entities of at least 3 characters are considered.
- No. named entities linked to DBpedia resources: 
    - titles: 277,783
    - abstracts: 1,558,119
- No. named entities linked to Wikidata resources: 
    - titles: nnn
    - abstracts: nnn


## Downloading and Querying
The dataset is available either as a Turtle dump in directory [dataset](/dataset), or through our Virtuoso SPARQL endpoint https://covid19.i3s.unice.fr/sparql.

You may use the [Faceted Browser](http://covid19.i3s.unice.fr:8890/fct/) to look up text or URIs.


## URIs

CORD-19 namespace is `http://ns.inria.fr/covid19/`.

The dataset itslef is identified by URI [`http://ns.inria.fr/covid19/dataset-1-0`](http://covid19.i3s.unice.fr:8890/describe/?url=http%3A%2F%2Fns.inria.fr%2Fcovid19%2Fdataset-1-0). It comes with DCAT and VOID descriptions.
All articles and annotations about named entities are linked back to the dataset with property `rdfs:isDefinedBy`.

Article URIs are formatted as `http://ns.inria.fr/covid19/paper_id` where paper_id may be either the article SHA hash or its PCM identifier.
Parts of an article (title, abstract and body) are also identified by URIs so that named entities can link back to the part they belong to. These URIs are formatted as 
- `http://ns.inria.fr/covid19/paper_id#title`
- `http://ns.inria.fr/covid19/paper_id#abstract`
- `http://ns.inria.fr/covid19/paper_id#body_text`.


## License

