import json
import requests
import traceback

from cord19_ner.utils.config import Config
from cord19_ner.utils.converter import Converter


class WrapperAnnotator(object):
    def __init__(self):
        self.dbpedia_spotlight_endpoint = Config.dbpedia_spotlight_endpoint
        self.entity_fishing_endpoint = Config.entity_fishing_endpoint
        self.ncbo_enpoint = Config.ncbo_endpoint

    def request_dbpedia_spotlight(self, text, confidence=0.15, support=10):
        """
        Wrapper around DBpedia Spotlight
        :param text: string, text to be annotated
        :param confidence: float, confidence score for disambiguation / linking
        :param support: integer, how prominent is this entity in Lucene Model, i.e. number of inlinks in Wikipedia
        :return: annotations in an Json array
        """
        try:
            headers = {'accept': 'application/json'}
            params = {
                'text': text,
                'confidence': confidence,
                'support': support,
            }
            response = requests.get(self.dbpedia_spotlight_endpoint, params=params, headers=headers)
            result = json.loads(response.text)["Resources"]
            result = [{x.replace('@', ''): Converter.string2number(v) for x, v in r.items()} for r in result]
            return result

        except Exception as err:
            traceback.print_tb(err.__traceback__)

    def request_entity_fishing(self, text):
        """
        Wrapper around Entity-fishing (language set in English)
        :param text: string, text to be annotated
        :return: annotations in JSON
        """
        try:
            files = {
                'query': (None,
                          '{ \'text\': ' + json.dumps(text) + ',\'language\':{\'lang\': \'en\'}}'),

            }

            response = requests.post(self.entity_fishing_endpoint + "disambiguate", files=files)
            return json.loads(response.text)

        except Exception as err:
            traceback.print_tb(err.__traceback__)

    # TODO identify the language of the article
    def request_get_language(self, text):
        try:
            params = {
                'text': text,
            }
            response = requests.get(self.entity_fishing_endpoint + "language", params=params)
            return json.loads(response.text)

        except Exception as err:
            traceback.print_tb(err.__traceback__)

    def request_ncbo(self, text, api_key=Config.ncbo_api_key):
        """
        Wrapper around the API of the Bioportal Annotator
        API link: http://data.bioontology.org/documentation
        :param text: string, text to br annotated
        :param api_key: string, API key to access the NCBO API Services
        :return: annotations in JSON
        """
        try:
            params = {
                'apikey': api_key,
                'text': text,
            }
            response = requests.get("http://data.bioontology.org/annotator", params=params)
            return json.loads(response.text)

        except Exception as err:
            traceback.print_tb(err.__traceback__)

    def request_ncbo_plus(self, text, api_key=Config.ncbo_api_key):
        """
        Wrapper around the API of the Bioportal AnnotatorPlus
        API link: http://data.bioontology.org/documentation
        :param text: string, text to be annotated
        :param api_key: string, API key to access the NCBO API Services
        :return: annotations in JSON
        """
        try:
            params = {
                'apikey': api_key,
                # options for clinical texts
                'negation': 'false',
                'experiencer': 'false',
                'temporality': 'false',
                # tweaks
                'lemmatize': 'true',
                'longest_only': 'true',
                # less verbose
                'display_links': 'false',
                'display_context': 'false',
                'text': text,
            }
            response = requests.get("http://services.data.bioontology.org/annotatorplus", params=params)
            return json.loads(response.text)

        except Exception as err:
            traceback.print_tb(err.__traceback__)

