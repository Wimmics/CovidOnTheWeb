import os


class Config(object):
    """
    Class that stores paths, endpoints and api keys.
    """
    project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Path to the CORD-19 dataset
    project_resources = "/data/CORD19"
    # Path where the annotated files will be saved
    corpus_annotated = "/data/CORD19-Annotation/"

    # Configuration of the different endpoints
    dbpedia_spotlight_endpoint = "http://localhost:2222/rest/annotate"
    entity_fishing_endpoint = "http://localhost:8090/service/"
    ncbo_endpoint = "http://data.bioontology.org/annotator"

    # API key of NCBO Bioportal
    ncbo_api_key = '###-###-###-###-###'

