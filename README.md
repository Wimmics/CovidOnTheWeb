# Covid-on-the-Web Dataset

*Covid-on-the-Web Dataset* is an RDF dataset that provides two main knowledge graphs produced by analyzing the scholarly articles of the [COVID-19 Open Research Dataset (CORD-19)](https://www.semanticscholar.org/cord19) [1], a resource of articles about COVID-19 and the coronavirus family of viruses:
- the *CORD-19 Named Entities Knowledge Graph* describes named entities identified and disambiguated by NCBO BioPortal annotator, Entity-fishing and DBpedia Spotlight. 
- the *CORD-19 Argumentative Knowledge Graph* describes argumentative components and PICO elements (Patient/Population/Problem, Intervention, Comparison, Outcome) extracted from the articles by the Argumentative Clinical Trial Analysis platform (ACTA).

A description of the dataset, in the Turtle format, as well as examples are provided in the [dataset](dataset) directory.

Covid-on-the-Web Dataset is an initiative of the [Wimmics team](https://team.inria.fr/wimmics/), [I3S laboratory](http://www.i3s.unice.fr/), University Côte d'Azur, Inria, CNRS.

Covid-on-the-Web Dataset **v1.1** is based on [CORD-19 v7](https://www.kaggle.com/dataset/08dd9ead3afd4f61ef246bfd6aee098765a19d9f6dbf514f0142965748be859b/version/7). 
 
#### I want it now: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3833753.svg)](https://doi.org/10.5281/zenodo.3833753)


### Documentation

- [RDF data modeling](doc/01-data-modeling.md)
- [Generation pipeline](src/README.md)


## CORD-19 Named Entities Knowledge Graph (CORD19-NEKG)

To identify and disambiguate named entities, we used [DBpedia Spotlight](https://www.dbpedia-spotlight.org/) (links to DBpedia), [Entity-fishing](https://github.com/kermitt2/entity-fishing) (links to Wikidata), and [NCBO BioPortal annotator](http://bioportal.bioontology.org/annotatorplus) (links to ontologies in Bioportal).

Named entities were identified primarily in the articles' titles and abstracts. Entity-fishing was also used to process the articles' bodies.

- Nb. of named entities linked to DBpedia resources:  1,792,748
- Nb. of named entities linked to Wikidata resources: 30,863,349
- Nb. of named entities linked to BioPortal ontologies: 21,874,798


## CORD-19 Argumentative Knowledge Graph (CORD19-AKG)

To extract argumentative components (claims and evidences) and PICO elements, we used the [Argumentative Clinical Trial Analysis](http://ns.inria.fr/acta/) platform (ACTA) [2].

Argumentative components and PICO elements were extracted from the articles' abstracts.

- Nb. of argumentative components: 53,871
- Nb. of PICO elements linked to UMLS concept IDs: 229,408


## URIs naming scheme

Covid-on-the-Web namespace is `http://ns.inria.fr/covid19/`. All URIs are dereferenceable.

The dataset itslef is identified by URI [`http://ns.inria.fr/covid19/covidontheweb-1-1`](http://ns.inria.fr/covid19/covidontheweb-1-1). It comes with DCAT and VOID descriptions.
All articles, annotations and arguments are linked back to the dataset with property `rdfs:isDefinedBy`.

Article URIs are formatted as `http://ns.inria.fr/covid19/paper_id` where paper_id may be either the article SHA hash or its PCM identifier.
Parts of an article (title, abstract and body) are also identified by URIs so that annotations of named entities can link back to the part they belong to. These URIs are formatted as 
- `http://ns.inria.fr/covid19/paper_id#title`
- `http://ns.inria.fr/covid19/paper_id#abstract`
- `http://ns.inria.fr/covid19/paper_id#body_text`.


## Downloading and SPARQL Querying

The dataset is downloadable as a set of RDF dumps (in Turtle syntax) from Zenodo: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3833753.svg)](https://doi.org/10.5281/zenodo.3833753)

It can also be queried through our Virtuoso OS SPARQL endpoint https://covidontheweb.inria.fr/sparql.

You may use the [Faceted Browser](http://covidontheweb.inria.fr/fct/) to look up text or URIs.
As an example, you can look up article [http://ns.inria.fr/covid19/f74923b3ce82c984a7ae3e0c2754c9e33c60554f](http://ns.inria.fr/covid19/f74923b3ce82c984a7ae3e0c2754c9e33c60554f).
Further details about how named entities are represented in RDF are given in the [Data Modeling](doc/01-data-modeling.md) section.

The following **named graphs** can be queried from our SPARQL endpoint:
- `http://ns.inria.fr/covid19/graph/metadata`: dataset description + definition of a few properties
- `http://ns.inria.fr/covid19/graph/articles`: articles metadata (title, authors, DOIs, journal etc.)
- `http://ns.inria.fr/covid19/graph/dbpedia-spotlight`: named entities identified by DBpedia Spotlight in articles titles/abstracts
- `http://ns.inria.fr/covid19/graph/entityfishing`: named entities identified by Entity-fishing in articles titles/abstracts
- `http://ns.inria.fr/covid19/graph/entityfishing/body`: named entities identified by Entity-fishing in articles bodies
- `http://ns.inria.fr/covid19/graph/bioportal-annotator`: named entities identified by Bioportal Annotator in articles titles/abstracts
- `http://ns.inria.fr/covid19/graph/acta`: argumentative components and PICO elements extracted by ACTA from articles titles/abstracts

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

See the [LICENSE file](LICENSE).

## Cite this work

When including Covid-on-the-Web data in a publication or redistribution, please cite the dataset as follows:

*Wimmics Research Team. Covid-on-the-Web Dataset. University Côte d'Azur, Inria, CNRS. 2020. Retrieved from https://github.com/Wimmics/CovidOnTheWeb.*


## References

[1] Wang, L.L., Lo, K., Chandrasekhar, Y., Reas, R., Yang, J., Eide, D., Funk, K., Kinney, R.M., Liu, Z., Merrill, W., Mooney, P., Murdick, D.A., Rishi, D., Sheehan, J., Shen, Z., Stilson, B., Wade, A.D., Wang, K., Wilhelm, C., Xie, B., Raymond, D.M., Weld, D.S., Etzioni, O., & Kohlmeier, S. (2020). CORD-19: The Covid-19 Open Research Dataset. ArXiv, abs/2004.10706.

[2] T. Mayer, E. Cabrio, and S. Villata. ACTA a tool for argumentative clinical trialanalysis. In Proceedings of the 28th International Joint Conference on  ArtificialIntelligence (IJCAI), pages 6551–6553, 2019.

