from covidontheweb_aug.query.linking import KnowledgeGraphRequest, Wrapper

from covidontheweb_aug.utils.config import Config
from covidontheweb_aug.utils.transcript import RDFTranscript
from covidontheweb_aug.utils.iodata import Output

if __name__ == '__main__':
    kg = KnowledgeGraphRequest()
    wrapper = Wrapper()

    rdf_translator = RDFTranscript()

    print("Generation of links associated with Wikidata entities.")
    entities_wikidata = kg.get_wikidata_entities()
    links_wikidata = kg.get_links_wikidata(entities_wikidata)
    g = rdf_translator.generate_linksets(rdf_translator.wikidata_uri)
    graph_closematch = rdf_translator.generate_closematch_relations(links_wikidata, rdf_translator.wikidata_uri, g)
    Output.save_rdf(graph_closematch, Config.corpus_annotated + "/wikidata_links.nt")

    print("Generation of links associated with PICO elements.")
    umls_cui = kg.get_pico_codes()
    print("--- Links from Wikidata.")
    links_pico = kg.get_links_pico(umls_cui)
    g = rdf_translator.generate_linksets(rdf_translator.umls_uri)
    print("--- Links from BioPortal.")
    links_pico_bioportal = wrapper.request_ncbo_with_cui(umls_cui)
    g = rdf_translator.generate_linksets_ncbo(rdf_translator.umls_uri, g)
    graph_closematch = rdf_translator.generate_closematch_relations(links_pico, rdf_translator.umls_uri, g)
    graph_closematch = rdf_translator.generate_closematch_relations(links_pico_bioportal, rdf_translator.umls_uri, g)
    Output.save_rdf(graph_closematch, Config.corpus_annotated + "/pico_links.nt")

    print("Generation of links associated with DBpedia entities.")
    entities_dbpedia = kg.get_dbpedia_entities()
    links_dbpedia = kg.get_links_dbpedia(entities_dbpedia)
    g = rdf_translator.generate_linksets(rdf_translator.dbpedia_uri)
    graph_closematch = rdf_translator.generate_closematch_relations(links_dbpedia, rdf_translator.dbpedia_uri, g)
    Output.save_rdf(graph_closematch, Config.corpus_annotated + "/dbpedia_links.nt")
