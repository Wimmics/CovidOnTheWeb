import urllib.parse

from rdflib import Graph, ConjunctiveGraph, URIRef, BNode, Literal
from rdflib.namespace import VOID, RDF, OWL, FOAF, RDFS, SKOS, DCTERMS, DCAT
from rdflib import Namespace

from covidontheweb_aug.utils.config import Config

class RDFTranscript(object):
    def __init__(self):
        self.covid = Namespace("http://ns.inria.fr/covid19/")

        self.coviddb_uri = URIRef(self.covid + "covidontheweb-1-1")
        self.dbpedia_uri = URIRef(self.covid + "DBpedia")
        self.wikidata_uri = URIRef(self.covid + "Wikidata")
        self.umls_uri = URIRef(self.covid + "UMLS")

    def generate_linksets(self, source):
        """
        Generate a Graph (rdflib) containing the datasets and linksets (VOID ontology).
        :param source: The URI of the Dataset from which resources come from
        :return g: a Graph with the different Linksets and Datasets
        """
        g = Graph()

        # Linkset between Covid Database and Wikidata
        cotw2dbpedia_linkset = URIRef(self.covid + "cotw2Wikidata")
        g.add((cotw2dbpedia_linkset, RDF.type, VOID.Linkset))
        g.add((cotw2dbpedia_linkset, VOID.target, self.coviddb_uri))
        g.add((cotw2dbpedia_linkset, VOID.target, self.wikidata_uri))
        g.add((cotw2dbpedia_linkset, VOID.linkPredicate, SKOS.closeMatch))

        # Linkset between DBpedia and Wikidata
        wikidata2dbpedia_linkset = URIRef(self.covid + "Wikidata2DBpedia")
        g.add((wikidata2dbpedia_linkset, RDF.type, VOID.Linkset))
        g.add((wikidata2dbpedia_linkset, VOID.target, self.wikidata_uri))
        g.add((wikidata2dbpedia_linkset, VOID.target, self.dbpedia_uri))
        g.add((wikidata2dbpedia_linkset, VOID.linkPredicate, SKOS.closeMatch))

        datasets_names = ["MAG", "YAGO", "Freebase_dump", "EOL", "MESH", "Google_KG", "Geonames",
                          "GBIF", "Semantic_Scholar", "UniProt", "IRMNG", "JSTOR", "Wikimedia_Commons", "VIAF",
                          "BNF", "ScOT", "ChemSpider", "EMBL-EBI", "ChemIDplus", "FDA", "NDL", "LOC", "MassBank",
                          "MoNA", "RxNav", "PDB", "THES_BNCF", "DrugBank", "Quora", "RCSB_PDB", "WikiSkripta",
                          "Britannica", "BabelNet", "Finto", "European_Commission", "Universalis", "ZTH", "DNB", "SFE",
                          "OmegaWiki", "FAST", "PSH", "Cultureel_Woordenboek", "FMA", "Ontobee", "Getty", "ICD9Data",
                          "ECY", "HPO", "uBio", "iNaturalist", "ITIS", "EPPO", "OSDB", "Bigenc", "ECHA", "NALT", "AUT",
                          "Iconclass", "Treccani", "Brockhaus", "Memory-alpha", "Nico_Nico_Pedia", "TA2",
                          "Enciclopedia", "IPNI", "Tropicos", "CJB", "Plants_Database", "PalDat", "Vikidia_ES",
                          "Vikidia_FR", "Vikidia_EU", "Vikidia_IT", "DBpedia_ES", "DBpedia_EU", "DBpedia_DE","DBpedia_IT",
                          "DBpedia_JA", "DBpedia_KO", "DBpedia_NL", "DBpedia_PL", "DBpedia_PT", "DBpedia_CS", "DBpedia_EL"]

        for d in datasets_names:
            temp_uri = URIRef(source + "2" + d)
            g.add((temp_uri, RDF.type, VOID.Linkset))
            g.add((temp_uri, VOID.target, source))
            g.add((temp_uri, VOID.target, URIRef(self.covid + d)))
            g.add((temp_uri, VOID.linkPredicate, SKOS.closeMatch))

        # DBpedia EN
        g.add((URIRef(self.dbpedia_uri), RDF.type, VOID.Dataset))
        g.add((URIRef(self.dbpedia_uri), FOAF.homepage, URIRef("http://dbpedia.org")))
        g.add((URIRef(self.dbpedia_uri), VOID.sparqlEndpoint, URIRef(Config.dbpedia_endpoint)))

        g.add((URIRef(self.covid + "DBpedia_FR"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "DBpedia_FR"), FOAF.homepage, URIRef("http://fr.dbpedia.org/")))
        g.add((URIRef(self.covid + "DBpedia_FR"), VOID.sparqlEndpoint, URIRef("http://fr.dbpedia.org/sparql")))

        g.add((URIRef(self.covid + "DBpedia_ES"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "DBpedia_ES"), FOAF.homepage, URIRef("http://es.dbpedia.org/")))
        g.add((URIRef(self.covid + "DBpedia_ES"), VOID.sparqlEndpoint, URIRef("http://es.dbpedia.org/sparql")))

        g.add((URIRef(self.covid + "DBpedia_EU"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "DBpedia_EU"), FOAF.homepage, URIRef("http://eu.dbpedia.org/")))
        g.add((URIRef(self.covid + "DBpedia_EU"), VOID.sparqlEndpoint, URIRef("https://eu.dbpedia.org/sparql")))

        g.add((URIRef(self.covid + "DBpedia_DE"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "DBpedia_DE"), FOAF.homepage, URIRef("http://de.dbpedia.org/")))
        g.add((URIRef(self.covid + "DBpedia_DE"), VOID.sparqlEndpoint, URIRef("https://de.dbpedia.org/sparql")))

        # Issue with this dataset
        g.add((URIRef(self.covid + "DBpedia_IT"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "DBpedia_IT"), FOAF.homepage, URIRef("http://it.dbpedia.org/")))
        g.add((URIRef(self.covid + "DBpedia_IT"), VOID.sparqlEndpoint, URIRef("http://it.dbpedia.org/sparql")))

        g.add((URIRef(self.covid + "DBpedia_JA"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "DBpedia_JA"), FOAF.homepage, URIRef("http://ja.dbpedia.org/")))
        g.add((URIRef(self.covid + "DBpedia_JA"), VOID.sparqlEndpoint, URIRef("http://ja.dbpedia.org/sparql")))

        # Issue with this dataset
        g.add((URIRef(self.covid + "DBpedia_KO"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "DBpedia_KO"), FOAF.homepage, URIRef("http://ko.dbpedia.org:8080/")))
        g.add((URIRef(self.covid + "DBpedia_KO"), VOID.sparqlEndpoint, URIRef("http://ko.dbpedia.org/sparql")))

        g.add((URIRef(self.covid + "DBpedia_NL"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "DBpedia_NL"), FOAF.homepage, URIRef("http://nl.dbpedia.org/")))
        g.add((URIRef(self.covid + "DBpedia_NL"), VOID.sparqlEndpoint, URIRef("http://nl.dbpedia.org/sparql")))

        g.add((URIRef(self.covid + "DBpedia_PL"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "DBpedia_PL"), FOAF.homepage, URIRef("http://pl.dbpedia.org/")))
        g.add((URIRef(self.covid + "DBpedia_PL"), VOID.sparqlEndpoint, URIRef("http://pl.dbpedia.org/sparql")))

        g.add((URIRef(self.covid + "DBpedia_PT"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "DBpedia_PT"), FOAF.homepage, URIRef("http://pt.dbpedia.org/")))
        g.add((URIRef(self.covid + "DBpedia_PT"), VOID.sparqlEndpoint, URIRef("http://pt.dbpedia.org/sparql")))

        g.add((URIRef(self.covid + "DBpedia_CS"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "DBpedia_CS"), FOAF.homepage, URIRef("http://cs.dbpedia.org/")))
        g.add((URIRef(self.covid + "DBpedia_CS"), VOID.sparqlEndpoint, URIRef("https://cs.dbpedia.org/sparql")))

        # Issue with this dataset
        g.add((URIRef(self.covid + "DBpedia_EL"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "DBpedia_EL"), FOAF.homepage, URIRef("http://el.dbpedia.org/")))
        g.add((URIRef(self.covid + "DBpedia_EL"), VOID.sparqlEndpoint, URIRef("https://el.dbpedia.org/sparql")))

        g.add((URIRef(self.wikidata_uri), RDF.type, VOID.Dataset))
        g.add((URIRef(self.wikidata_uri), FOAF.homepage, URIRef("https://wikidata.org")))
        g.add((URIRef(self.wikidata_uri), VOID.sparqlEndpoint, URIRef(Config.wikidata_endpoint)))

        # UMLS
        g.add((URIRef(self.umls_uri), RDF.type, VOID.Dataset))
        g.add((URIRef(self.umls_uri), FOAF.homepage, URIRef("https://uts-ws.nlm.nih.gov/home.html")))
        g.add((URIRef(self.umls_uri), FOAF.homepage, URIRef("https://ncim-stage.nci.nih.gov/ncimbrowser/")))
        g.add((URIRef(self.umls_uri), VOID.uriLookupEndpoint, URIRef("https://uts-ws.nlm.nih.gov/rest/")))

        # MAG
        g.add((URIRef(self.covid + "MAG"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "MAG"), FOAF.homepage, URIRef("https://academic.microsoft.com/home")))
        g.add((URIRef(self.covid + "MAG"), VOID.sparqlEndpoint, URIRef("http://ma-graph.org/sparql")))
        g.add((URIRef(self.covid + "MAG"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q60683589")))

        # YAGO
        g.add((URIRef(self.covid + "YAGO"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "YAGO"), VOID.sparqlEndpoint, URIRef("https://yago-knowledge.org/sparql")))
        g.add((URIRef(self.covid + "YAGO"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q8045810")))

        # Freebase Dump
        g.add((URIRef(self.covid + "Freebase_Dump"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Freebase_Dump"), FOAF.homepage, URIRef("https://tools.wmflabs.org/freebase/")))
        # Broader object
        g.add((URIRef(self.covid + "Freebase_Dump"), RDFS.seeAlso, URIRef("http://www.wikidata.org/entity/Q36500248")))

        # Dautsche National Bibliothek
        g.add((URIRef(self.covid + "DNB"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "DNB"), FOAF.homepage, URIRef("https://www.dnb.de/EN/Home/home_node.html")))

        # Encyclopedia of Life
        g.add((URIRef(self.covid + "EOL"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "EOL"), FOAF.homepage, URIRef("https://eol.org/")))
        g.add((URIRef(self.covid + "EOL"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q82486")))

        # MESH
        g.add((URIRef(self.covid + "MESH"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "MESH"), FOAF.homepage, URIRef("https://id.nlm.nih.gov/mesh/")))
        g.add((URIRef(self.covid + "MESH"), VOID.sparqlEndpoint, URIRef("https://id.nlm.nih.gov/mesh/query")))

        # GOOGLE KG
        g.add((URIRef(self.covid + "Google_KG"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Google_KG"), FOAF.homepage, URIRef("https://developers.google.com/knowledge-graph")))
        g.add((URIRef(self.covid + "Google_KG"), VOID.uriLookupEndpoint, URIRef("https://kgsearch.googleapis.com/v1/entities:search")))

        # Geonames
        g.add((URIRef(self.covid + "Geonames"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Geonames"), FOAF.homepage, URIRef("http://www.geonames.org/")))
        g.add((URIRef(self.covid + "Geonames"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q830106")))

        # Global Biodiversity Information Facility
        g.add((URIRef(self.covid + "GBIF"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "GBIF"), FOAF.homepage, URIRef("https://www.gbif.org/")))
        g.add((URIRef(self.covid + "GBIF"), VOID.uriLookupEndpoint, URIRef("https://api.gbif.org/v1/")))
        g.add((URIRef(self.covid + "GBIF"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q1531570")))

        # Semantic Scholar
        g.add((URIRef(self.covid + "Semantic_Scholar"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Semantic_Scholar"), FOAF.homepage, URIRef("https://www.semanticscholar.org/")))
        g.add((URIRef(self.covid + "Semantic_Scholar"), VOID.uriLookupEndpoint, URIRef("https://api.semanticscholar.org/v1/")))
        g.add((URIRef(self.covid + "Semantic_Scholar"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q22908627")))

        # UniProt
        g.add((URIRef(self.covid + "UniProt"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "UniProt"), FOAF.homepage, URIRef("https://www.uniprot.org/")))
        g.add((URIRef(self.covid + "UniProt"), VOID.sparqlEndpoint, URIRef("https://sparql.uniprot.org/sparql")))
        g.add((URIRef(self.covid + "UniProt"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q905695")))

        # IRMNG
        g.add((URIRef(self.covid + "IRMNG"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "IRMNG"), FOAF.homepage, URIRef("https://www.irmng.org/")))
        g.add((URIRef(self.covid + "IRMNG"), VOID.uriLookupEndpoint, URIRef("https://www.irmng.org/rest/")))
        g.add((URIRef(self.covid + "IRMNG"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q51885189")))

        # JSTOR
        g.add((URIRef(self.covid + "JSTOR"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "JSTOR"), FOAF.homepage, URIRef("https://www.jstor.org/")))
        g.add((URIRef(self.covid + "JSTOR"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q1420342")))

        # Wikimedia Commons
        g.add((URIRef(self.covid + "Wikimedia_Commons"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Wikimedia_Commons"), FOAF.homepage, URIRef("https://commons.wikimedia.org/wiki/Main_Page")))
        g.add((URIRef(self.covid + "Wikimedia_Commons"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q565")))

        # VIAF
        g.add((URIRef(self.covid + "VIAF"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "VIAF"), FOAF.homepage, URIRef("https://viaf.org/")))
        g.add((URIRef(self.covid + "VIAF"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q54919")))

        # BNF
        g.add((URIRef(self.covid + "BNF"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "BNF"), FOAF.homepage, URIRef("https://www.bnf.fr/")))
        g.add((URIRef(self.covid + "BNF"), VOID.sparqlEndpoint, URIRef("https://data.bnf.fr/sparql")))
        g.add((URIRef(self.covid + "BNF"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q193563")))

        # ScOT Vocabulary Curriculum
        g.add((URIRef(self.covid + "ScOT"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "ScOT"), FOAF.homepage, URIRef("http://scot.curriculum.edu.au/")))
        g.add((URIRef(self.covid + "ScOT"), VOID.sparqlEndpoint, URIRef("http://vocabulary.curriculum.edu.au/PoolParty/sparql/scot")))
        g.add((URIRef(self.covid + "ScOT"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q65000093")))

        g.add((URIRef(self.covid + "ChemSpider"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "ChemSpider"), FOAF.homepage, URIRef("http://www.chemspider.com/")))
        g.add((URIRef(self.covid + "ChemSpider"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q2311683")))

        g.add((URIRef(self.covid + "EMBL-EBI"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "EMBL-EBI"), FOAF.homepage, URIRef("https://www.ebi.ac.uk/")))
        g.add((URIRef(self.covid + "EMBL-EBI"), VOID.sparqlEndpoint, URIRef("https://www.ebi.ac.uk/rdf/services/sparql")))
        g.add((URIRef(self.covid + "EMBL-EBI"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q1341845")))

        g.add((URIRef(self.covid + "OSDB"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "OSDB"), FOAF.homepage, URIRef("http://www.osdb.info/")))
        g.add((URIRef(self.covid + "OSDB"), VOID.uriLookupEndpoint, URIRef("http://www.osdb.info/")))
        g.add((URIRef(self.covid + "OSDB"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q27301274")))

        g.add((URIRef(self.covid + "ChemIDplus"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "ChemIDplus"), FOAF.homepage, URIRef("https://chem.nlm.nih.gov/chemidplus/")))
        g.add((URIRef(self.covid + "ChemIDplus"), VOID.uriLookupEndpoint, URIRef("https://chem.nlm.nih.gov/api/data/")))
        g.add((URIRef(self.covid + "ChemIDplus"), VOID.uriLookupEndpoint, URIRef("https://chem.nlm.nih.gov/api/data/")))
        g.add((URIRef(self.covid + "ChemIDplus"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q20593")))

        g.add((URIRef(self.covid + "FDA"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "FDA"), FOAF.homepage, URIRef("https://fdasis.nlm.nih.gov/srs/")))

        g.add((URIRef(self.covid + "NDL"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "NDL"), FOAF.homepage, URIRef("https://www.ndl.go.jp/")))
        g.add((URIRef(self.covid + "NDL"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q477675")))

        g.add((URIRef(self.covid + "LOC"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "LOC"), FOAF.homepage, URIRef("https://www.loc.gov/")))
        g.add((URIRef(self.covid + "LOC"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q131454")))

        g.add((URIRef(self.covid + "MassBank"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "MassBank"), FOAF.homepage, URIRef("https://massbank.eu/MassBank/")))
        g.add((URIRef(self.covid + "MassBank"), VOID.uriLookupEndpoint, URIRef("https://massbank.eu/MassBank/Result.jsp")))
        g.add((URIRef(self.covid + "MassBank"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q24088019")))

        g.add((URIRef(self.covid + "MoNA"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "MoNA"), FOAF.homepage, URIRef("https://mona.fiehnlab.ucdavis.edu/")))
        g.add((URIRef(self.covid + "MoNA"), VOID.uriLookupEndpoint, URIRef("https://mona.fiehnlab.ucdavis.edu/rest/spectra/search")))

        g.add((URIRef(self.covid + "RxNav"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "RxNav"), FOAF.homepage, URIRef("https://mor.nlm.nih.gov/RxNav/")))
        g.add((URIRef(self.covid + "RxNav"), VOID.uriLookupEndpoint, URIRef("https://rxnav.nlm.nih.gov/REST/rxcui.json")))

        g.add((URIRef(self.covid + "PDB"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "PDB"), FOAF.homepage, URIRef("https://www.wwpdb.org/")))
        g.add((URIRef(self.covid + "PDB"), VOID.uriLookupEndpoint, URIRef("https://integbio.jp/rdf/sparql")))
        g.add((URIRef(self.covid + "MassBank"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q8036801")))

        g.add((URIRef(self.covid + "SML"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "SML"), FOAF.homepage, URIRef("https://sml.snl.no/")))
        g.add((URIRef(self.covid + "SML"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q19378370")))

        g.add((URIRef(self.covid + "THES_BNCF"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "THES_BNCF"), FOAF.homepage, URIRef("https://thes.bncf.firenze.sbn.it/")))
        g.add((URIRef(self.covid + "THES_BNCF"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q16583225")))

        g.add((URIRef(self.covid + "DrugBank"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "DrugBank"), FOAF.homepage, URIRef("https://www.drugbank.ca/")))
        g.add((URIRef(self.covid + "DrugBank"), VOID.sparqlEndpoint, URIRef("hhttp://wifo5-04.informatik.uni-mannheim.de/drugbank/sparql")))
        g.add((URIRef(self.covid + "DrugBank"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q1122544")))

        g.add((URIRef(self.covid + "Quora"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Quora"), FOAF.homepage, URIRef("https://quora.com/")))
        g.add((URIRef(self.covid + "Quora"), VOID.uriLookupEndpoint, URIRef("https://api.quora.com/api")))
        g.add((URIRef(self.covid + "Quora"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q51711")))

        g.add((URIRef(self.covid + "RCSB_PDB"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "RCSB_PDB"), FOAF.homepage, URIRef("https://www.rcsb.org/")))
        g.add((URIRef(self.covid + "RCSB_PDB"), VOID.uriLookupEndpoint, URIRef("https://data.rcsb.org/rest/v1/core/")))
        g.add((URIRef(self.covid + "RCSB_PDB"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q55823721")))

        g.add((URIRef(self.covid + "WikiSkripta"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "WikiSkripta"), FOAF.homepage, URIRef("https://www.wikiskripta.eu/w/Home")))
        g.add((URIRef(self.covid + "WikiSkripta"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q9049250")))

        g.add((URIRef(self.covid + "Britannica"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Britannica"), FOAF.homepage, URIRef("https://www.britannica.com/")))
        g.add((URIRef(self.covid + "Britannica"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q455")))

        g.add((URIRef(self.covid + "BabelNet"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "BabelNet"), FOAF.homepage, URIRef("https://babelnet.org/")))
        g.add((URIRef(self.covid + "BabelNet"), VOID.sparqlEndpoint, URIRef("https://babelnet.org/sparql/")))
        g.add((URIRef(self.covid + "BabelNet"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q4837690")))

        g.add((URIRef(self.covid + "Finto"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Finto"), FOAF.homepage, URIRef("http://finto.fi/fi/#maincontent")))
        g.add((URIRef(self.covid + "Finto"), VOID.uriLookupEndpoint, URIRef("http://api.finto.fi/rest/v1/")))
        g.add((URIRef(self.covid + "Finto"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q61677804")))

        g.add((URIRef(self.covid + "European_Commission"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "European_Commission"), FOAF.homepage, URIRef("https://ec.europa.eu/info/index_en")))
        g.add((URIRef(self.covid + "European_Commission"), VOID.sparqlEndpoint, URIRef("https://data.europa.eu/euodp/en/sparqlep")))
        g.add((URIRef(self.covid + "European_Commission"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q8880")))

        g.add((URIRef(self.covid + "Universalis"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Universalis"), FOAF.homepage, URIRef("https://www.universalis.fr/")))
        g.add((URIRef(self.covid + "Universalis"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q1340194")))

        g.add((URIRef(self.covid + "ZTH"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "ZTH"), FOAF.homepage, URIRef("https://zthiztegia.elhuyar.eus/")))

        g.add((URIRef(self.covid + "SFE"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "SFE"), FOAF.homepage, URIRef("http://www.sf-encyclopedia.com/")))

        g.add((URIRef(self.covid + "OmegaWiki"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "OmegaWiki"), FOAF.homepage, URIRef("http://www.omegawiki.org/Meta:Main_Page")))
        g.add((URIRef(self.covid + "OmegaWiki"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q154436")))

        g.add((URIRef(self.covid + "FAST"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "FAST"), FOAF.homepage, URIRef("http://experimental.worldcat.org/fast/")))

        # Polythematic Structured Subject Heading System
        g.add((URIRef(self.covid + "PSH"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "PSH"), FOAF.homepage, URIRef("https://psh.techlib.cz/skos/")))
        g.add((URIRef(self.covid + "PSH"), VOID.uriLookupEndpoint, URIRef("https://psh.techlib.cz/api/concepts")))

        # Cultureel Woordenboek
        g.add((URIRef(self.covid + "Cultureel_Woordenboek"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Cultureel_Woordenboek"), FOAF.homepage, URIRef("https://www.cultureelwoordenboek.nl/")))
        g.add((URIRef(self.covid + "Cultureel_Woordenboek"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q3010887")))

        # FMA Browser
        g.add((URIRef(self.covid + "FMA"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "FMA"), FOAF.homepage, URIRef("http://fma.si.washington.edu/browser/#/")))
        g.add((URIRef(self.covid + "FMA"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q1406710")))

        g.add((URIRef(self.covid + "Ontobee"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Ontobee"), FOAF.homepage, URIRef("http://www.ontobee.org/")))
        g.add((URIRef(self.covid + "Ontobee"), VOID.sparqlEndpoint, URIRef("http://www.ontobee.org/sparql")))
        g.add((URIRef(self.covid + "Ontobee"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q47069651")))

        g.add((URIRef(self.covid + "Getty"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Getty"), FOAF.homepage, URIRef("http://vocab.getty.edu/")))
        g.add((URIRef(self.covid + "Getty"), VOID.sparqlEndpoint, URIRef("http://vocab.getty.edu/sparql")))
        g.add((URIRef(self.covid + "Getty"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q5554720")))

        g.add((URIRef(self.covid + "ICD9Data"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "ICD9Data"), FOAF.homepage, URIRef("http://www.icd9data.com/")))

        # ECY Encyclopedia of Modern UKraine
        g.add((URIRef(self.covid + "ECY"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "ECY"), FOAF.homepage, URIRef("http://esu.com.ua/")))
        g.add((URIRef(self.covid + "ECY"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q4532152")))

        # HPO Human Phenotype Ontology
        g.add((URIRef(self.covid + "HPO"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "HPO"), FOAF.homepage, URIRef("https://hpo.jax.org/app/")))

        g.add((URIRef(self.covid + "uBio"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "uBio"), FOAF.homepage, URIRef("http://www.ubio.org/")))
        g.add((URIRef(self.covid + "uBio"), VOID.uriLookupEndpoint, URIRef("http://ubio.org/webservices/service.php?function=")))
        g.add((URIRef(self.covid + "uBio"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q3551271")))

        g.add((URIRef(self.covid + "iNaturalist"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "iNaturalist"), FOAF.homepage, URIRef("https://www.inaturalist.org/")))
        g.add((URIRef(self.covid + "iNaturalist"), VOID.uriLookupEndpoint, URIRef("https://www.inaturalist.org/")))
        g.add((URIRef(self.covid + "iNaturalist"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q16958215")))

        g.add((URIRef(self.covid + "ITIS"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "ITIS"), FOAF.homepage, URIRef("https://www.itis.gov/")))
        g.add((URIRef(self.covid + "ITIS"), VOID.uriLookupEndpoint, URIRef("https://www.itis.gov/ITISWebService/")))
        g.add((URIRef(self.covid + "ITIS"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q82575")))

        g.add((URIRef(self.covid + "EPPO"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "EPPO"), FOAF.homepage, URIRef("https://gd.eppo.int/")))
        g.add((URIRef(self.covid + "EPPO"), VOID.uriLookupEndpoint, URIRef("https://data.eppo.int/api/rest/1.0/")))

        g.add((URIRef(self.covid + "Bigenc"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Bigenc"), FOAF.homepage, URIRef("https://bigenc.ru/")))
        g.add((URIRef(self.covid + "Bigenc"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q1768199")))

        g.add((URIRef(self.covid + "ECHA"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "ECHA"), FOAF.homepage, URIRef("https://echa.europa.eu/")))
        g.add((URIRef(self.covid + "ECHA"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q59911453")))

        # National Agricultural Library's Agricultural Thesaurus
        g.add((URIRef(self.covid + "NALT"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "NALT"), FOAF.homepage, URIRef("https://agclass.nal.usda.gov/")))
        g.add((URIRef(self.covid + "NALT"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q17364107")))

        # STW Thesaurus for Economics
        g.add((URIRef(self.covid + "STW"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "STW"), FOAF.homepage, URIRef("https://zbw.eu/stw/version/latest/about")))
        g.add((URIRef(self.covid + "STW"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q26903352")))

        # AUT Databáze národních autorit NK ČR
        g.add((URIRef(self.covid + "AUT"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "AUT"), FOAF.homepage, URIRef("https://aleph.nkp.cz/F/?func=find-c&local_base=aut")))
        g.add((URIRef(self.covid + "AUT"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q13550863")))

        g.add((URIRef(self.covid + "Iconclass"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Iconclass"), FOAF.homepage, URIRef("http://iconclass.org/")))
        g.add((URIRef(self.covid + "Iconclass"), VOID.uriLookupEndpoint, URIRef("http://iconclass.org/json/?notation=")))
        g.add((URIRef(self.covid + "Iconclass"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q13550863")))

        g.add((URIRef(self.covid + "Treccani"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Treccani"), FOAF.homepage, URIRef("http://www.treccani.it/")))
        g.add((URIRef(self.covid + "Treccani"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q731361")))

        g.add((URIRef(self.covid + "Brockhaus"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Brockhaus"), FOAF.homepage, URIRef("https://brockhaus.de/info/")))
        g.add((URIRef(self.covid + "Brockhaus"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q237227")))

        g.add((URIRef(self.covid + "Memory-alpha"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Memory-alpha"), FOAF.homepage, URIRef("https://memory-alpha.fandom.com/wiki/Portal:Main")))
        g.add((URIRef(self.covid + "Memory-alpha"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q498824")))

        g.add((URIRef(self.covid + "Nico_Nico_Pedia"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Nico_Nico_Pedia"), FOAF.homepage, URIRef("https://dic.nicovideo.jp/?from=header")))
        g.add((URIRef(self.covid + "Nico_Nico_Pedia"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q10856286")))

        g.add((URIRef(self.covid + "TA2"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "TA2"), FOAF.homepage, URIRef("https://ta2viewer.openanatomy.org/")))

        # enciclopedia catala
        g.add((URIRef(self.covid + "Enciclopedia"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Enciclopedia"), FOAF.homepage, URIRef("https://www.enciclopedia.cat/")))

        # Intenational Plant Names Index
        g.add((URIRef(self.covid + "IPNI"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "IPNI"), FOAF.homepage, URIRef("https://ipni.org/")))
        g.add((URIRef(self.covid + "IPNI"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q922063")))

        g.add((URIRef(self.covid + "Tropicos"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Tropicos"), FOAF.homepage, URIRef("http://legacy.tropicos.org/Home.aspx")))
        g.add((URIRef(self.covid + "Tropicos"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q2578548")))

        # CJB Conservatory and Botanical Garden of the City of Geneva
        g.add((URIRef(self.covid + "CJB"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "CJB"), FOAF.homepage, URIRef("http://www.ville-ge.ch/cjb/")))
        g.add((URIRef(self.covid + "CJB"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q677516")))

        # Plants Database
        g.add((URIRef(self.covid + "Plants_Database"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Plants_Database"), FOAF.homepage, URIRef("https://plants.sc.egov.usda.gov/java/")))

        # Palynological Database
        g.add((URIRef(self.covid + "PalDat"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "PalDat"), FOAF.homepage, URIRef("https://www.paldat.org/")))
        g.add((URIRef(self.covid + "PalDat"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q59786289")))

        g.add((URIRef(self.covid + "Vikidia_ES"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Vikidia_ES"), FOAF.homepage, URIRef("https://es.vikidia.org/wiki/Vikidia:Portada")))

        g.add((URIRef(self.covid + "Vikidia_FR"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Vikidia_FR"), FOAF.homepage, URIRef("https://fr.vikidia.org/wiki/Vikidia:Accueil")))

        g.add((URIRef(self.covid + "Vikidia_EU"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Vikidia_EU"), FOAF.homepage, URIRef("https://eu.vikidia.org/wiki/Azala")))

        g.add((URIRef(self.covid + "Vikidia_IT"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "Vikidia_IT"), FOAF.homepage, URIRef("https://it.vikidia.org/wiki/Pagina_principale")))

        return g

    def generate_linksets_ncbo(self, source, g=None):
        """
        Generate a Graph (rdflib) containing the datasets and linksets (VOID ontology) of BioPortal.
        :param source: The URI of the Dataset from which resources come from
        :return g: a Graph with the different Linksets and Datasets
        """
        if not g:
            g = Graph()

        datasets_names = ["NDF-RT", "MDRFRE", "MEDRA", "ICD10CM", "OCHV", "DOID", "SNOMEDCT", "SCTSPA", "NANDO", "PDO",
                          "SNMI", "CST", "CRISP", "WHO-ART", "RCTV2", "WHOFRE", "OMIM", "RADLEX", "ICPC2P", "MESH",
                          "GAMUTS", "CHEBI", "RXNORM", "DrugBank", "JGLOBAL", "ADO", "VANDF", "IOBC", "ATC", "NDDF",
                          "DRON", "ICPC2P", "NCIT", "MP", "SYMP", "EFO"]

        for d in datasets_names:
            temp_uri = URIRef(source + "2" + d)
            g.add((temp_uri, RDF.type, VOID.Linkset))
            g.add((temp_uri, VOID.target, source))
            g.add((temp_uri, VOID.target, URIRef(self.covid + d)))
            g.add((temp_uri, VOID.linkPredicate, SKOS.closeMatch))

        g.add((URIRef(self.covid + "NDF-RT"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "NDF-RT"), FOAF.homepage, URIRef("https://evs.nci.nih.gov/ftp1/NDF-RT/")))
        g.add((URIRef(self.covid + "NDF-RT"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/NDFRT")))
        g.add((URIRef(self.covid + "NDF-RT"), DCTERMS.hasVersion, Literal("05.07.2018-2018AA")))

        g.add((URIRef(self.covid + "MDRFRE"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "MDRFRE"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/MDRFRE")))
        g.add((URIRef(self.covid + "MDRFRE"), DCTERMS.hasVersion, Literal("11.04.2019-2019AB")))
        g.add((URIRef(self.covid + "MDRFRE"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/MDRFRE/submissions/15/download")))

        g.add((URIRef(self.covid + "MEDRA"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "MEDRA"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/MEDDRA")))
        g.add((URIRef(self.covid + "MEDRA"), FOAF.homepage, URIRef("https://www.meddra.org/")))
        g.add((URIRef(self.covid + "MEDRA"), DCTERMS.hasVersion, Literal("11.04.2019-2019AB")))

        g.add((URIRef(self.covid + "ICD10CM"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "ICD10CM"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/ICD10CM")))
        g.add((URIRef(self.covid + "ICD10CM"), DCTERMS.hasVersion, Literal("11.04.2019-2019AB")))
        g.add((URIRef(self.covid + "ICD10CM"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/ICD10CM/submissions/17/download")))

        g.add((URIRef(self.covid + "OCHV"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "OCHV"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/OCHV")))
        g.add((URIRef(self.covid + "OCHV"), DCTERMS.hasVersion, Literal("01.21.2016-1")))
        g.add((URIRef(self.covid + "OCHV"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/OCHV/submissions/2/download")))

        g.add((URIRef(self.covid + "DOID"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "DOID"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/DOID")))
        g.add((URIRef(self.covid + "DOID"), DCTERMS.hasVersion, Literal("03.02.2018-releases/2018-03-02")))
        g.add((URIRef(self.covid + "DOID"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/DOID/download")))

        g.add((URIRef(self.covid + "RCD"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "RCD"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/RCD")))
        g.add((URIRef(self.covid + "RCD"), DCTERMS.hasVersion, Literal("11.04.2019-2019AB")))

        g.add((URIRef(self.covid + "SNOMEDCT"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "SNOMEDCT"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/SNOMEDCT")))
        g.add((URIRef(self.covid + "SNOMEDCT"), DCTERMS.hasVersion, Literal("11.04.2019-2019AB")))

        g.add((URIRef(self.covid + "SCTSPA"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "SCTSPA"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/SCTSPA")))
        g.add((URIRef(self.covid + "SCTSPA"), DCTERMS.hasVersion, Literal("11.04.2019-2019AB")))

        g.add((URIRef(self.covid + "NANDO"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "NANDO"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/NANDO")))
        g.add((URIRef(self.covid + "NANDO"), FOAF.homepage, URIRef("http://nanbyodata.jp/ontology/nando")))
        g.add((URIRef(self.covid + "NANDO"), DCTERMS.hasVersion, Literal("07.01.2020-0.4.0")))
        g.add((URIRef(self.covid + "NANDO"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/NANDO/submissions/10/download")))

        g.add((URIRef(self.covid + "PDO"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "PDO"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/PDO")))
        g.add((URIRef(self.covid + "PDO"), DCTERMS.hasVersion, Literal("03.31.2016-Version 0.7")))
        g.add((URIRef(self.covid + "PDO"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/PDO/submissions/6/download")))

        g.add((URIRef(self.covid + "SNMI"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "SNMI"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/SNMI")))
        g.add((URIRef(self.covid + "SNMI"), DCTERMS.hasVersion, Literal("11.04.2019-2019AB")))
        g.add((URIRef(self.covid + "SNMI"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/SNMI/submissions/15/download")))

        g.add((URIRef(self.covid + "CST"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "CST"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/CST")))
        g.add((URIRef(self.covid + "CST"), DCTERMS.hasVersion, Literal("05.13.2018-unknown")))
        g.add((URIRef(self.covid + "CST"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/CST/submissions/1/download")))

        # CSP
        g.add((URIRef(self.covid + "CRISP"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "CRISP"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/CRISP")))
        g.add((URIRef(self.covid + "CRISP"), DCTERMS.hasVersion, Literal("11.04.2019-2019AB")))
        g.add((URIRef(self.covid + "CRISP"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/CRISP/submissions/15/download")))

        g.add((URIRef(self.covid + "WHO-ART"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "WHO-ART"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/WHO-ART")))
        g.add((URIRef(self.covid + "WHO-ART"), DCTERMS.hasVersion, Literal("11.04.2019-2019AB")))

        g.add((URIRef(self.covid + "RCTV2"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "RCTV2"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/RCTV2")))
        g.add((URIRef(self.covid + "RCTV2"), DCTERMS.hasVersion, Literal("04.11.2016-2015")))
        g.add((URIRef(self.covid + "RCTV2"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/RCTV2/submissions/1/download")))

        g.add((URIRef(self.covid + "WHOFRE"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "WHOFRE"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/WHOFRE")))
        g.add((URIRef(self.covid + "WHOFRE"), DCTERMS.hasVersion, Literal("11.04.2019-2019AB")))
        g.add((URIRef(self.covid + "WHOFRE"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/WHOFRE/submissions/15/download")))

        g.add((URIRef(self.covid + "OMIM"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "OMIM"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/OMIM")))
        g.add((URIRef(self.covid + "OMIM"), DCTERMS.hasVersion, Literal("11.04.2019-2019AB")))
        g.add((URIRef(self.covid + "OMIM"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/OMIM/submissions/17/download")))

        g.add((URIRef(self.covid + "RADLEX"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "RADLEX"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/RADLEX")))
        g.add((URIRef(self.covid + "RADLEX"), FOAF.homepage, URIRef("http://radlex.org/")))
        g.add((URIRef(self.covid + "RADLEX"), DCTERMS.hasVersion, Literal("03.20.2018-4.0")))
        g.add((URIRef(self.covid + "RADLEX"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/RADLEX/submissions/39/download")))

        g.add((URIRef(self.covid + "ICPC2P"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "ICPC2P"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/ICPC2P")))
        g.add((URIRef(self.covid + "ICPC2P"), DCTERMS.hasVersion, Literal("11.04.2019-2019AB")))

        g.add((URIRef(self.covid + "MESH"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "MESH"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/ICPC2P")))
        g.add((URIRef(self.covid + "MESH"), DCTERMS.hasVersion, Literal("11.04.2019-2019AB")))
        g.add((URIRef(self.covid + "MESH"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/MESH/submissions/19/download")))

        g.add((URIRef(self.covid + "GAMUTS"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "GAMUTS"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/GAMUTS")))
        g.add((URIRef(self.covid + "GAMUTS"), DCTERMS.hasVersion, Literal("10.15.2018-0.91")))
        g.add((URIRef(self.covid + "GAMUTS"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/GAMUTS/submissions/23/download")))

        g.add((URIRef(self.covid + "CHEBI"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "CHEBI"), FOAF.homepage, URIRef("https://www.ebi.ac.uk/chebi/")))
        g.add((URIRef(self.covid + "CHEBI"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/CHEBI")))
        g.add((URIRef(self.covid + "CHEBI"), DCTERMS.hasVersion, Literal("06.30.2020-189")))
        g.add((URIRef(self.covid + "CHEBI"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/CHEBI/download&download_format=rdf")))

        g.add((URIRef(self.covid + "RXNORM"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "RXNORM"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/RXNORM")))
        g.add((URIRef(self.covid + "RXNORM"), DCTERMS.hasVersion, Literal("11.04.2019-2019AB")))
        g.add((URIRef(self.covid + "RXNORM"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/RXNORM/submissions/18/download")))

        g.add((URIRef(self.covid + "DrugBank"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "DrugBank"), FOAF.homepage, URIRef("https://www.drugbank.ca/")))
        g.add((URIRef(self.covid + "DrugBank"), VOID.sparqlEndpoint, URIRef("hhttp://wifo5-04.informatik.uni-mannheim.de/drugbank/sparql")))
        g.add((URIRef(self.covid + "DrugBank"), SKOS.closeMatch, URIRef("http://www.wikidata.org/entity/Q1122544")))

        # Veterans Health Administration National Drug File
        g.add((URIRef(self.covid + "VANDF"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "VANDF"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/VANDF")))
        g.add((URIRef(self.covid + "VANDF"), DCTERMS.hasVersion, Literal("11.04.2019-2019AB")))
        g.add((URIRef(self.covid + "VANDF"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/VANDF/submissions/15/download")))

        # Alzheimer's disease ontology
        g.add((URIRef(self.covid + "ADO"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "ADO"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/ADO")))
        g.add((URIRef(self.covid + "ADO"), DCTERMS.hasVersion, Literal("07.23.2013-1.1.1")))
        g.add((URIRef(self.covid + "ADO"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/ADO/submissions/3/download")))

        g.add((URIRef(self.covid + "JGLOBAL"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "JGLOBAL"), FOAF.homepage, URIRef("https://jglobal.jst.go.jp/en")))

        # Interlinking Ontology for Biological Concepts
        g.add((URIRef(self.covid + "IOBC"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "IOBC"), FOAF.homepage, URIRef("https://github.com/kushidat/IOBC")))
        g.add((URIRef(self.covid + "IOBC"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/IOBC")))
        g.add((URIRef(self.covid + "IOBC"), DCTERMS.hasVersion, Literal("09.02.2019-version 1.4.0")))
        g.add((URIRef(self.covid + "IOBC"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/IOBC/submissions/23/download")))

        g.add((URIRef(self.covid + "ATC"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "ATC"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/ATC")))
        g.add((URIRef(self.covid + "ATC"), DCTERMS.hasVersion, Literal("11.04.2019-2019AB")))
        g.add((URIRef(self.covid + "ATC"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/ATC/submissions/12/download")))

        g.add((URIRef(self.covid + "NDDF"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "NDDF"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/NDDF")))
        g.add((URIRef(self.covid + "NDDF"), DCTERMS.hasVersion, Literal("11.04.2019-2019AB")))

        g.add((URIRef(self.covid + "DRON"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "DRON"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/DRON")))
        g.add((URIRef(self.covid + "DRON"), DCTERMS.hasVersion, Literal("07.04.2020-2020-06-01")))
        g.add((URIRef(self.covid + "DRON"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/DRON/submissions/12/download")))

        g.add((URIRef(self.covid + "ICPC2P"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "ICPC2P"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/DRON")))
        g.add((URIRef(self.covid + "ICPC2P"), DCTERMS.hasVersion, Literal("11.04.2019-2019AB")))

        g.add((URIRef(self.covid + "NCIT"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "NCIT"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/NCIT")))
        g.add((URIRef(self.covid + "NCIT"), DCTERMS.hasVersion, Literal("06.29.2020-20.06e")))
        g.add((URIRef(self.covid + "NCIT"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/NCIT/submissions/93/download")))

        # Mammalian Phenotype Ontology
        g.add((URIRef(self.covid + "MP"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "MP"), FOAF.homepage, URIRef("http://www.ontobee.org/ontology/MP")))

        g.add((URIRef(self.covid + "SYMP"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "SYMP"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/SYMP")))
        g.add((URIRef(self.covid + "SYMP"), FOAF.homepage, URIRef("http://www.ontobee.org/ontology/SYMP")))
        g.add((URIRef(self.covid + "SYMP"), DCTERMS.hasVersion, Literal("02.26.2020-unknown")))
        g.add((URIRef(self.covid + "SYMP"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/SYMP/submissions/22/download")))

        # Experimental Factor Ontology
        g.add((URIRef(self.covid + "EFO"), RDF.type, VOID.Dataset))
        g.add((URIRef(self.covid + "EFO"), FOAF.homepage, URIRef("https://bioportal.bioontology.org/ontologies/EFO")))
        g.add((URIRef(self.covid + "EFO"), FOAF.homepage, URIRef("https://www.ebi.ac.uk/ols/ontologies/efo")))
        g.add((URIRef(self.covid + "EFO"), DCTERMS.hasVersion, Literal("02.26.2020-unknown")))
        g.add((URIRef(self.covid + "EFO"), DCAT.downloadURL, URIRef("http://data.bioontology.org/ontologies/SYMP/submissions/22/download")))

        return g

    def generate_closematch_relations(self, linkset, source, g=None):
        """
        Generate a Graph (rdflib) with skos:closeMatch relations from a set containing links
        :param linkset: set with a key as resource and a list with the associated links as value
        :param source: The URI of the Dataset from which resources come from
        :param g: An existing Graph (rdflib)
        :return g: Graph with skos:closeMatch relations
        """
        if not g:
            g = Graph()
        for key, value in linkset.items():
            # Attach an entity to a Dataset
            g.add((URIRef(key), VOID.inDataset, URIRef(source)))
            for v in value:
                # Handle SKOS.closeMatch relations
                g.add((URIRef(key), SKOS.closeMatch, URIRef(urllib.parse.quote(v, safe=",:?!/_#=&()%\'"))))
        return g
