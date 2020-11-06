import os


class Config(object):
    """
    Class that stores paths, endpoints and api keys.
    """
    DOWNLOAD_CORPUS = False

    # Options to run NER tools
    DBPEDIA_SPOTLIGHT = False
    ENTITY_FISHING = False
    NCBO_BIOPORTAL = False

    project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Path to the CORD-19 dataset
    project_resources = "/data/document_parses"
    # Path where the annotated files will be saved
    corpus_annotated = "/data/CORD19-Annotation/"

    # Configuration of the different endpoints
    dbpedia_spotlight_endpoint = {
        'en': "http://localhost:2222/rest/annotate",
        'de': "http://localhost:2223/rest/annotate",
        'fr': "http://localhost:2224/rest/annotate",
        'es': "http://localhost:2225/rest/annotate",
        'it': "http://localhost:2226/rest/annotate"
    }
    entity_fishing_endpoint = "http://localhost:8090/service/"

    ncbo_annotatorplus = {
        # API key of BioPortal: https://bioportal.bioontology.org/ // English endpoint
        'en': ("XXX-XXX-XXX", "http://services.data.bioontology.org/annotatorplus"),
        # API key of SIFR BioPortal: http://bioportal.lirmm.fr/ // French endpoint
        'fr': ("XXX-XXX-XXX", "http://services.bioportal.lirmm.fr/annotatorplus")
    }
