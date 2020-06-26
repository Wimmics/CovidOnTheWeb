from covidontheweb_aug.query.get_links import KnowledgeGraphRequest

from covidontheweb_aug.utils.config import Config
from covidontheweb_aug.utils.transcript import RDFTranscript
from covidontheweb_aug.utils.iodata import Output

if __name__ == '__main__':
    kg = KnowledgeGraphRequest()
    rdf_translator = RDFTranscript()

    # Retrieve the links associated with the Wikidata entities
    print("Generation of links associated with Wikidata entities.")
    entities_wikidata = kg.get_wikidata_entities()
    links_wikidata = kg.get_links_wikidata(entities_wikidata)
    g = rdf_translator.generate_linksets(rdf_translator.wikidata_uri)
    graph_sameas = rdf_translator.generate_closematch_relations(links_wikidata, rdf_translator.wikidata_uri, g)
    Output.save_rdf(graph_sameas, Config.corpus_annotated + "/wikidata_links.nt")

    # Retrieve the links associated with the PICO elements
    print("Generation of links associated with PICO elements.")
    umls_cui = kg.get_pico_codes()
    links_pico = kg.get_links_pico(umls_cui)
    graph_sameas = rdf_translator.generate_closematch_relations(links_pico, rdf_translator.umls_uri, g)
    Output.save_rdf(graph_sameas, Config.corpus_annotated + "/pico_links.nt")

    # Retrieve the links associated with the DBpedia entities
    print("Generation of links associated with DBpedia entities.")
    entities_dbpedia = kg.get_dbpedia_entities()
    links_dbpedia = kg.get_links_dbpedia(entities_dbpedia)
    graph_sameas = rdf_translator.generate_closematch_relations(links_dbpedia, rdf_translator.dbpedia_uri, g)
    Output.save_rdf(graph_sameas, Config.corpus_annotated + "/dbpedia_links.nt")
