import os


class Config(object):
    """
    Class that stores paths and endpoints.
    """
    project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Path to the CORD-19 dataset
    project_resources = "/data/CORD19"
    # Path where the annotated files will be saved
    corpus_annotated = "/data/CORD19-Annotation/"

    # Configuration of the different endpoints
    corese_endpoint = "http://localhost:2500/sparql"
    covidOnTheWeb_endpoint = "https://covid19.i3s.unice.fr/sparql"
    wikidata_endpoint = "https://query.wikidata.org/sparql"
    dbpedia_endpoint = "http://dbpedia.org/sparql"


    umls_namespace = "https://uts-ws.nlm.nih.gov/rest/semantic-network/2015AB/CUI/"

    # API key of NCBO Bioportal
    ncbo_api_key = '###-###-###-###-###'
