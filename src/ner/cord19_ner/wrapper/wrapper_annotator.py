import json
import requests
import traceback

from cord19_ner.utils.config import Config
from cord19_ner.utils.converter import Converter


class WrapperAnnotator(object):
    def __init__(self):
        self.dbpedia_spotlight_endpoint = Config.dbpedia_spotlight_endpoint
        self.entity_fishing_endpoint = Config.entity_fishing_endpoint
        self.ncbo_enpoint_annotatorplus = Config.ncbo_annotatorplus

    def request_dbpedia_spotlight(self, text, lang='en', confidence=0.15, support=10):
        """
        Wrapper around DBpedia Spotlight
        :param text: String, text to be annotated
        :param lang: string, language model to use
        :param confidence: float, confidence score for disambiguation / linking
        :param support: integer, how prominent is this entity in Lucene Model, i.e. number of inlinks in Wikipedia
        :return: annotations in an Json array
        """
        try:
            if lang not in ('en', 'de', 'fr', 'es', 'it'):
                lang = 'en'

            headers = {'accept': 'application/json'}
            params = {
                'text': text,
                'confidence': confidence,
                'support': support,
            }
            # not supported by get if text too long
            response = requests.post(self.dbpedia_spotlight_endpoint[lang], data=params, headers=headers)
            result = json.loads(response.text)["Resources"]
            result = [{x.replace('@', ''): Converter.string2number(v) for x, v in r.items()} for r in result]
            return result

        # null
        except json.decoder.JSONDecodeError:
            return None

    def request_entity_fishing(self, text, lang='en'):
        """
        Wrapper around Entity-fishing (language set in English)
        :param text: string, text to be annotated
        :param lang: string, language model to use
        :return: annotations in JSON
        """
        try:
            if lang not in ('en', 'de', 'fr', 'es', 'it'):
                lang = 'en'

            files = {
                'query': (
                          '{ \'text\': ' + json.dumps(text) + ',\'language\':{\'lang\': \'' + lang + '\'}}'),
            }

            response = requests.post(self.entity_fishing_endpoint + "disambiguate", files=files)
            return json.loads(response.text)

        # null
        except json.decoder.JSONDecodeError:
            return None

    def request_ncbo_plus(self, text, lang='en', ncbo_api=Config.ncbo_annotatorplus):
        """
        Wrapper around the API of the Bioportal AnnotatorPlus
        API link: http://data.bioontology.org/documentation
        :param text: String, text to be annotated
        :param ncbo_api: Dict, Contains a list with API key to access the NCBO API Web Service and the endpoint
        :param lang: string, language model to use
        :return: annotations in JSON
        """
        try:
            if lang not in ('en', 'fr'):
                lang = 'en'
            params = {
                'apikey': ncbo_api[lang][0],
                # options for clinical texts
                'negation': 'false',
                'experiencer': 'false',
                'temporality': 'false',
                # tweaks
                'longest_only': 'true',
                # less verbose
                'display_links': 'false',
                'display_context': 'false',
                'text': text,
            }
            # Option not supported in French
            if lang == 'en':
                params["lemmatize"] = 'true'

            response = requests.get(ncbo_api[lang][1], params=params)
            return json.loads(response.text)

        # null
        except json.decoder.JSONDecodeError:
            return None
