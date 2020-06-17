# Covid-On-The-Web RDF Data Modeling

The description of each article from the CORD-19 corpus comes in three parts: (1) metadata such as title and authors, (2) annotations about named entities, and (3) argumentative components and PICO elements. Below we exemplify and described these parts.

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

@prefix aif:    <http://www.arg.dundee.ac.uk/aif#>.    # Argument Interchange Format
@prefix amo:    <http://purl.org/spar/amo/>.           # Argument Model Ontology (Toulmin)
@prefix sioca:  <http://rdfs.org/sioc/argument#>.      # SIOC Argumentation Module
@prefix umls:   <http://bioportal.bioontology.org/ontologies/umls/>.

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
- license (`dct:license`)
- identifiers
    - DOI (`bibo:doi`)
    - Pubmed identifer (`bibo:pmid` and `fabio:hasPubMedId`)
    - PMC identifer (`fabio:hasPubMedCentralId`)
- source of the metadata information (`dct:source`)
- DOI-based URL (`schema:url`)
- SHA hash (`foaf:sha1`)

Furthermore, each article is linked to its parts (title, abstract, body) as follows:
- `covidpr:hasTitle <http://ns.inria.fr/covid19/paper_id#title>`
- `dct:abstract     <http://ns.inria.fr/covid19/paper_id#abstract>`
- `covidpr:hasBody  <http://ns.inria.fr/covid19/paper_id#body_text>`.

Here is an example of article metadata:
```turtle
<http://ns.inria.fr/covid19/f74923b3ce82c984a7ae3e0c2754c9e33c60554f>
    a                   fabio:ResearchPaper, bibo:AcademicArticle, schema:ScholarlyArticle;
    rdfs:isDefinedBy    <http://ns.inria.fr/covid19/dataset-1-1>;
    dct:title           "A real-time PCR for SARS-coronavirus incorporating target gene pre-amplification";
    schema:publication  "Biochemical and Biophysical Research Communications";
    dce:creator	        "Wong, Freda Pui-Fan", "Tam, Siu-Lun", "Fung, Yin-Wan", "Li, Hui", "Cheung, Albert", "Chan, Paul", "Lin, Sau-Wah", "Collins, Richard", "Dillon, Natalie";
    dct:source          "Elsevier";
    dct:license         "els-covid";

    dct:issued          "2003-12-26"^^xsd:date;
    bibo:doi            "10.1016/j.bbrc.2003.11.064";
    bibo:pmid           "14652014";
    fabio:hasPubMedId   "14652014";
    foaf:sha1           "f74923b3ce82c984a7ae3e0c2754c9e33c60554f";
    schema:url          <https://doi.org/10.1016/j.bbrc.2003.11.064>;
    
    dct:abstract        <http://ns.inria.fr/covid19/f74923b3ce82c984a7ae3e0c2754c9e33c60554f#abstract>;
    covidpr:hasTitle    <http://ns.inria.fr/covid19/f74923b3ce82c984a7ae3e0c2754c9e33c60554f#title>;
    covidpr:hasBody     <http://ns.inria.fr/covid19/f74923b3ce82c984a7ae3e0c2754c9e33c60554f#body_text>.
```

## Named entities

The named entities identified in an article are described as **annotations** using the **[Web Annotations Vocabulary](https://www.w3.org/TR/annotation-vocab/)**.
Each annotation consists of the following information:
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

## Argumentative components and PICO elements

The arguments extracted from an article are described using the [Argument Model Ontology](http://purl.org/spar/amo/), [SIOC Argumentation Module](http://rdfs.org/sioc/argument#) and [Argument Interchange Format](http://www.arg.dundee.ac.uk/aif#).

In the example below, an argument is defined that consits of 3 components: 2 evidences and a claim, with support/attack relations between the components:
```turtle
<http://ns.inria.fr/covid19/arg/4f8d24c531d2c334969e09e4b5aed66dcc925c4b>
    a                   amo:Argument;
    schema:about        covid:f74923b3ce82c984a7ae3e0c2754c9e33c60554f;
    dct:creator         <https://team.inria.fr/wimmics/>;
    prov:wasGeneratedBy	covid:ProvenanceActa.

    # Argumentative components
    amo:hasEvidence     <http://ns.inria.fr/covid19/arg/4f8d24c531d2c334969e09e4b5aed66dcc925c4b/0>;
    amo:hasEvidence     <http://ns.inria.fr/covid19/arg/4f8d24c531d2c334969e09e4b5aed66dcc925c4b/123>;
    amo:hasClaim        <http://ns.inria.fr/covid19/arg/4f8d24c531d2c334969e09e4b5aed66dcc925c4b/6>;
   .

<http://ns.inria.fr/covid19/arg/4f8d24c531d2c334969e09e4b5aed66dcc925c4b/0>
    a                   amo:Evidence, sioca:Justification, aif:I-node;
    prov:wasQuotedFrom  covid:4f8d24c531d2c334969e09e4b5aed66dcc925c4b;
    aif:formDescription "17 patients discharged in recovered condition and 10 patients died in hospital."^^xsd:string;
    # evidence 0 supports claim 6
    sioca:supports      <http://ns.inria.fr/covid19/arg/4f8d24c531d2c334969e09e4b5aed66dcc925c4b/6>;
    amo:proves          <http://ns.inria.fr/covid19/arg/4f8d24c531d2c334969e09e4b5aed66dcc925c4b/6>.
    .

<http://ns.inria.fr/covid19/arg/4f8d24c531d2c334969e09e4b5aed66dcc925c4b/123>
    a                   amo:Evidence, sioca:Justification, aif:I-node;
    prov:wasQuotedFrom  covid:4f8d24c531d2c334969e09e4b5aed66dcc925c4b;
    aif:formDescription "some other evidence"^^xsd:string;
    # evidence 123 attacks claim 6
    sioca:challenges <http://ns.inria.fr/covid19/arg/4f8d24c531d2c334969e09e4b5aed66dcc925c4b/6>.
    .

<http://ns.inria.fr/covid19/arg/4f8d24c531d2c334969e09e4b5aed66dcc925c4b/6>
    a                   amo:Claim, sioca:Idea, aif:I-node, aif:KnowledgePosition_Statement;
    prov:wasQuotedFrom  covid:4f8d24c531d2c334969e09e4b5aed66dcc925c4b;
    aif:claimText       "a simple ct scoring method was capable to predict mortality."^^xsd:string;
    .
```


PICO elements identified in an argumentative component are described in a way very similar to the named entities, using the **[Web Annotations Vocabulary](https://www.w3.org/TR/annotation-vocab/)**. The annotation bodies provide UMLS concepts and term ids.

Example:
```turtle
[]  a                   oa:Annotation;
    schema:about        <http://ns.inria.fr/covid19/4f8d24c531d2c334969e09e4b5aed66dcc925c4b>;
    covidpr:confidence  1^^xsd:decimal;

    # link to the ULMS concept id (CUI) and semantic type id (TUI)
    oa:hasBody          [ umls:cui "C0026565"; umls:tui "T81" ];
    oa:hasTarget [
        # the source is the claim/evidence
        oa:hasSource    <http://ns.inria.fr/covid19/arg/4f8d24c531d2c334969e09e4b5aed66dcc925c4b/6>;
        oa:hasSelector  [
            a           oa:TextQuoteSelector;
            oa:exact    "mortality";
        ]
    ].
```



## Provenance information

Provenance information about each annotation provides the annotation author (`dct:creator`), source dataset and version (`prov:used`, CORD-19 v6 in the example below), and the tool used to identify the named entity (`prov:wasAssociatedWith`, entity-fishing in the example below).

```turtle
_:b40150806
    rdfs:isDefinedBy    <http://ns.inria.fr/covid19/dataset-1-1>;
    dct:creator         <https://team.inria.fr/wimmics/>;
    prov:wasGeneratedBy [
        a               prov:Activity;
        prov:used       <http://ns.inria.fr/covid19/cord19v7>;
        prov:wasAssociatedWith <https://github.com/kermitt2/entity-fishing>.
    ].

<http://ns.inria.fr/covid19/cord19v7>
    a                    schema:Dataset dcat:Dataset;
    owl:versionInfo      "7";
    dct:title            "COVID-19 Open Research Dataset (CORD-19)";
    dct:issued           "2020-04-10"^^xsd:date;
    schema:url           <https://www.kaggle.com/dataset/08dd9ead3afd4f61ef246bfd6aee098765a19d9f6dbf514f0142965748be859b/version/7>.
```
