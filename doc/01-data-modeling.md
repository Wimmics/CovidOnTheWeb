# CORD19-NEKG Data Modeling

The description of each article comes in two parts: (1) metadata and (2) annotations about named entities. These are exemplified below.

## Namespaces

Below we use the following namespaces:

```turtle
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#>.
@prefix owl:    <http://www.w3.org/2002/07/owl#>.
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .

@prefix bibo:   <http://purl.org/ontology/bibo/> .
@prefix dce:    <http://purl.org/dc/elements/1.1/>.
@prefix dct:    <http://purl.org/dc/terms/>.
@prefix fabio:  <http://purl.org/spar/fabio/> .
@prefix foaf:   <http://xmlns.com/foaf/0.1/>.
@prefix frbr:   <http://purl.org/vocab/frbr/core#>.
@prefix oa:     <http://www.w3.org/ns/oa#>.
@prefix prov:   <http://www.w3.org/ns/prov#>.
@prefix schema: <http://schema.org/>.

@prefix covid:  <http://ns.inria.fr/covid19/>.
@prefix covidpr:<http://ns.inria.fr/covid19/property/>.
```

## Article metadata

Article metadata such as the title, authors, journal, DOI, PCM identifer etc. are represented as exemplified:

```turtle
<http://ns.inria.fr/covid19/f74923b3ce82c984a7ae3e0c2754c9e33c60554f>
    a                   fabio:ResearchPaper, bibo:AcademicArticle, schema:ScholarlyArticle;
    rdfs:isDefinedBy    <http://ns.inria.fr/covid19/dataset-1-0>;
    dct:title           "A real-time PCR for SARS-coronavirus incorporating target gene pre-amplification";
    schema:publication  "Biochemical and Biophysical Research Communications";
    dct:source          "Elsevier";

    dct:issued          "2003-12-26"^^xsd:dateTime;
    bibo:doi            "10.1016/j.bbrc.2003.11.064";
    bibo:pmid           "14652014";
    fabio:hasPubMedId   "14652014";
    foaf:sha1           "f74923b3ce82c984a7ae3e0c2754c9e33c60554f";
    schema:url          <https://doi.org/10.1016/j.bbrc.2003.11.064>;
    
    dct:abstract        <http://ns.inria.fr/covid19/f74923b3ce82c984a7ae3e0c2754c9e33c60554f#abstract>;
    covidpr:hasTitle    <http://ns.inria.fr/covid19/f74923b3ce82c984a7ae3e0c2754c9e33c60554f#title>;
    covidpr:hasBody     <http://ns.inria.fr/covid19/f74923b3ce82c984a7ae3e0c2754c9e33c60554f#body_text>.
```

## Article named entities

The named entities identified in an article are described as annotations using the [Web Annotations Vocabulary](https://www.w3.org/TR/annotation-vocab/).

Each annotation is a blank node related to the article in two ways:
- it is about (schema:about) the article URI
- the annotation's target (`oa:hasTarget`) has as a source (`oa:hasSource`) the article title URI

```turtle
_:b24095433
    a                   oa:Annotation, prov:Entity;
    rdfs:isDefinedBy    <http://ns.inria.fr/covid19//dataset-1-0>;
    schema:about        <http://ns.inria.fr/covid19/f74923b3ce82c984a7ae3e0c2754c9e33c60554f>;
    dct:creator         <https://team.inria.fr/wimmics/>;

    oa:hasBody          <http://dbpedia.org/resource/SARS_coronavirus>;
    oa:hasTarget        [
        oa:hasSource    <http://ns.inria.fr/covid19/f74923b3ce82c984a7ae3e0c2754c9e33c60554f#abstract>;
        oa:hasSelector  [
            a           oa:TextPositionSelector, oa:TextQuoteSelector;
            oa:exact    "comorbidities";
            oa:start    "446"
        ]
    ];
    covidpr:confidence  1^^xsd:decimal.
```

## Provenance information

Provenance information about each annotation consists of the source dataset and version (CORD-19 v6 in the example below), and the tool used to identify the named entity (DBpedia Spotlight in the example below).

```turtle
_:b24095433
    prov:wasGeneratedBy    [
        a               prov:Activity;
        prov:used       <http://ns.inria.fr/covid19/cord19v6>;
        prov:wasAssociatedWith <https://www.dbpedia-spotlight.org/>.
    ].

<http://ns.inria.fr/covid19/cord19v6>
    a                    schema:Dataset dcat:Dataset;
    owl:versionInfo      "6";
    dct:title            "COVID-19 Open Research Dataset (CORD-19)";
    dct:issued           "2020-04-03"^^xsd:gYear;
    schema:url           <https://www.kaggle.com/dataset/08dd9ead3afd4f61ef246bfd6aee098765a19d9f6dbf514f0142965748be859b/version/6>.
```
