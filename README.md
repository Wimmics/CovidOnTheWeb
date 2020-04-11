# CORD-19 Named Entities Knowlegde Graph (CORD19-NEKG)

CORD-19 Named Entities Knowlegde Graph (CORD19-NEKG) is an RDF dataset describing named entities identified in the scholarly articles of the [COVID-19 Open Research Dataset (CORD-19)](https://pages.semanticscholar.org/coronavirus-research) [1], a resource of over 47,000 articles about COVID-19 and the coronavirus family of viruses.

CORD19-NEKG is an initiative of the [Wimmics team](https://team.inria.fr/wimmics/), [I3S laboratory](http://www.i3s.unice.fr/), Université Côte d'Azur, CNRS, Inria.
RDF files are generated using [Morph-xR2RML](https://github.com/frmichel/morph-xr2rml/), an implementation of the [xR2RML mapping language](http://i3s.unice.fr/~fmichel/xr2rml_specification.html) [2].


#### Documentation

- [RDF Data Modeling](doc/01-data-modeling.md)
- [Generation Pipeline](doc/02-generation-pipeline.md)


## Named Entities

To identify and disambiguate named entities, we used [DBpedia Spotlight](https://www.dbpedia-spotlight.org/) (links to DBpedia), [entity-fishing](https://github.com/kermitt2/entity-fishing) (links to Wikidata), and [NCBO BioPortal annotator](http://bioportal.bioontology.org/annotatorplus) (links to ontologies in Bioportal).

CORD19-NEKG **v1.0** is based on [CORD-19 v6](https://www.kaggle.com/dataset/08dd9ead3afd4f61ef246bfd6aee098765a19d9f6dbf514f0142965748be859b/version/6). It provides named entities identified by DBpedia Spotlight and entity-fishing in articles titles and abstracts, and only named entities of at least 3 characters are considered.
- No. named entities linked to DBpedia resources: 
    - titles: 277,783
    - abstracts: 1,558,119
    - **total: 1,835,902**
- No. named entities linked to Wikidata resources: 
    - titles: 145,706
    - abstracts: 645,216
    - **total: 790,922**


## URIs to name things

CORD19-NEKG namespace is `http://ns.inria.fr/covid19/`.

The dataset itslef is identified by URI `http://ns.inria.fr/covid19/dataset-1-0` ([describe](http://covid19.i3s.unice.fr:8890/describe/?url=http%3A%2F%2Fns.inria.fr%2Fcovid19%2Fdataset-1-0)). It comes with DCAT and VOID descriptions.
All articles and annotations about named entities are linked back to the dataset with property `rdfs:isDefinedBy`.

Article URIs are formatted as `http://ns.inria.fr/covid19/paper_id` where paper_id may be either the article SHA hash or its PCM identifier.
Parts of an article (title, abstract and body) are also identified by URIs so that annotations of named entities can link back to the part they belong to. These URIs are formatted as 
- `http://ns.inria.fr/covid19/paper_id#title`
- `http://ns.inria.fr/covid19/paper_id#abstract`
- `http://ns.inria.fr/covid19/paper_id#body_text`.


## Downloading and SPARQL Querying

The dataset is available either as a Turtle dump in the [dataset](/dataset) directory, or through our Virtuoso OS SPARQL endpoint https://covid19.i3s.unice.fr/sparql.

You may use the [Faceted Browser](http://covid19.i3s.unice.fr:8890/fct/) to look up text or URIs.
As an example, you can [look up article http://ns.inria.fr/covid19/f74923b3ce82c984a7ae3e0c2754c9e33c60554f](http://covid19.i3s.unice.fr:8890/describe/?url=http%3A%2F%2Fns.inria.fr%2Fcovid19%2Ff74923b3ce82c984a7ae3e0c2754c9e33c60554f&sid=50&urilookup=1).
Further details about how named entities are represented in RDF are given in the [Data Modeling](doc/01-data-modeling.md) section.

The following **named graphs** can be queried from our SPARQL endpoint:
- `http://ns.inria.fr/covid19/graph/metadata`: dataset description + definition of a few properties
- `http://ns.inria.fr/covid19/graph/articles`: articles metadata (title, authors, DOIs, journal etc.)
- `http://ns.inria.fr/covid19/graph/dbpedia-spotlight`: named entities identified by DBpedia Spotlight
- `http://ns.inria.fr/covid19/graph/entityfishing`: named entities identified by Entity-fishing

The example query below retrieves two articles that have been annotated with at least one common Wikidata entity.
```sparql
select ?uri ?title1 ?title2
where {
  graph <http://ns.inria.fr/covid19/graph/articles> {
    ?paper1 a fabio:ResearchPaper; dct:title ?title1.
    ?paper2 a fabio:ResearchPaper; dct:title ?title2.
    filter (?paper1 != ?paper2)
  }
  
  graph <http://ns.inria.fr/covid19/graph/entityfishing> {
    ?a1 a oa:Annotation;
        schema:about ?paper1;
        oa:hasBody ?uri.
    ?a2 a oa:Annotation;
        schema:about ?paper2;
        oa:hasBody ?uri.
  }
} limit 10
```


## License

This CORD-19 Named Entities Knowlegde Graph dataset (CORD19-NEKG) was derived from the CORD-19 dataset.
It consists of two subsets:
- the CORD-19 dataset itself, translated into the Turtle RDF syntax, subject to the CORD-19 license; and
- the result of a text mining process meant to extract named entities.

The CORD19-NEKG dataset is therefore licensed under two licenses, each applying to the aforementioned subsets:
- The CORD-19 license (https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-13/COVID.DATA.LIC.AGMT.pdf) applies to the CORD-19 dataset that is contained in the CORD19-NEKG dataset (as a subset translated into the Turtle RDF syntax).   
- The Open Data Commons Attribution License (http://opendatacommons.org/licenses/by/1.0) applies to the subset of the CORD19-NEKG dataset that results of a text mining process, that does not contain the aforementioned CORD-19 subset.


## Cite this work

When including CORD19-NEKG data in a publication or redistribution, please cite the dataset as follows:

*R. Gazzotti, F. Michel, F. Gandon. CORD-19 Named Entities Knowlegde Graph (CORD19-NEKG). University Côte d'Azur, Inria, CNRS. 2020. Retrieved from https://github.com/Wimmics/cord19-nekg.*


## References

[1] COVID-19 Open Research Dataset (CORD-19). 2020. Version 2020-04-03. Retrieved from https://pages.semanticscholar.org/coronavirus-research. Accessed 2020-04-06. doi:10.5281/zenodo.3715505

[2] F. Michel, L. Djimenou, C. Faron-Zucker, and J. Montagnat. Translation of Relational and Non-Relational Databases into RDF with xR2RML. In Proceedings of the *11th International Confenrence on Web Information Systems and Technologies (WEBIST 2015)*, Lisbon, Portugal, 2015.
