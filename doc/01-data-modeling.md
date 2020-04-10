# CORD19-NEKG Data Modeling

The description of each article comes in two parts: (1) metadata such as title and authors, and (2) annotations about named entities. Below we exemplify and described these parts.

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

Article URIs are formatted as `http://ns.inria.fr/covid19/paper_id` where paper_id may be either the article SHA hash or its PCM identifier.

Article metadata includes the following items:
- title (`dct:title`)
- authors (`dce:creator`)
- publication date (`dct:issued`)
- journal (`schema:publication`)
- identifiers
    - DOI (`bibo:doi`)
    - Pubmed identifer (`bibo:pmid` and `fabio:hasPubMedId`)
    - PMC identifer (`fabio:hasPubMedCentralId`)
- source of the metadata information (`dct:source`)
- DOI-based URL (`schema:url`)
- SHA hash (`foaf:sha1`)

Furthermore, each article is linked to its parts (title, abstract, body) as follows:
- `dct:abstract     <http://ns.inria.fr/covid19/paper_id#title>`
- `covidpr:hasTitle <http://ns.inria.fr/covid19/paper_id#abstract>`
- `covidpr:hasBody  <http://ns.inria.fr/covid19/paper_id#body_text>`.

Here is an example of article metadata:
```turtle
<http://ns.inria.fr/covid19/f74923b3ce82c984a7ae3e0c2754c9e33c60554f>
    a                   fabio:ResearchPaper, bibo:AcademicArticle, schema:ScholarlyArticle;
    rdfs:isDefinedBy    <http://ns.inria.fr/covid19/dataset-1-0>;
    dct:title           "A real-time PCR for SARS-coronavirus incorporating target gene pre-amplification";
    schema:publication  "Biochemical and Biophysical Research Communications";
    dce:creator	        "Wong, Freda Pui-Fan", "Tam, Siu-Lun", "Fung, Yin-Wan", "Li, Hui", "Cheung, Albert", "Chan, Paul", "Lin, Sau-Wah", "Collins, Richard", "Dillon, Natalie";
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

The named entities identified in an article are described as **annotations** using the **[Web Annotations Vocabulary](https://www.w3.org/TR/annotation-vocab/)**.
Each annotation is a blank node consisting of the following information:
- the article it is about (`schema:about`)
- the annotation target (`oa:hasTarget`) describes the piece of text identified as a named entity as follows:
    - the source (`oa:hasSource`) is the part of the article where the named entity was detected
    - the selecor (`oa:hasSelector`) gives the named entity raw text (`oa:exact`) and its location whithin the source (`oa:start` and `oa:end`)
- the annotation body (`oa:hasBody`) gives the URI of the resource identified as representing the named entity (e.g. a Wikidata URI)
- domains related to the named entity (`dct:subject`)

Example:
```turtle
_:b40150806	
    a                   oa:Annotation, prov:Entity;
    schema:about        <http://ns.inria.fr/covid19/f74923b3ce82c984a7ae3e0c2754c9e33c60554f>;
    dct:subject         "Engineering", "Biology";
    
    covidpr:confidence	"1"^^xsd:decimal;
    oa:hasBody          <http://wikidata.org/entity/Q176996>;
    oa:hasTarget [
        oa:hasSource    <http://ns.inria.fr/covid19/f74923b3ce82c984a7ae3e0c2754c9e33c60554f#abstract>;
        oa:hasSelector  [
            a           oa:TextPositionSelector, oa:TextQuoteSelector;
            oa:exact    "PCR";
            oa:start    "235";
            oa:end      "238"
        ]
    ];
```

## Provenance information

Provenance information about each annotation provides the annotation author (`dct:creator`), source dataset and version (`prov:used`, CORD-19 v6 in the example below), and the tool used to identify the named entity (`prov:wasAssociatedWith`, entity-fishing in the example below).

```turtle
_:b40150806
    rdfs:isDefinedBy    <http://ns.inria.fr/covid19/dataset-1-0>;
    dct:creator         <https://team.inria.fr/wimmics/>;
    prov:wasGeneratedBy [
        a               prov:Activity;
        prov:used       <http://ns.inria.fr/covid19/cord19v6>;
        prov:wasAssociatedWith <https://github.com/kermitt2/entity-fishing>.
    ].

<http://ns.inria.fr/covid19/cord19v6>
    a                    schema:Dataset dcat:Dataset;
    owl:versionInfo      "6";
    dct:title            "COVID-19 Open Research Dataset (CORD-19)";
    dct:issued           "2020-04-03"^^xsd:gYear;
    schema:url           <https://www.kaggle.com/dataset/08dd9ead3afd4f61ef246bfd6aee098765a19d9f6dbf514f0142965748be859b/version/6>.
```
