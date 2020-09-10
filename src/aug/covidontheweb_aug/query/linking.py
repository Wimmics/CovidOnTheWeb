import concurrent.futures
import json
import traceback
from math import ceil

import tqdm

import requests
from SPARQLWrapper import SPARQLWrapper, JSON

from covidontheweb_aug.utils.config import Config

class KnowledgeGraphRequest(object):
    # TODO handle BioPortal entities
    def __init__(self):
        # Endpoints
        self.covidOnTheWeb_endpoint = Config.covidOnTheWeb_endpoint
        self.wikidata_endpoint = Config.wikidata_endpoint
        self.dbpedia_endpoint = Config.dbpedia_endpoint

        self.dbpedia_entities = []
        self.wikidata_entities = []
        self.pico_codes = []

    def get_dbpedia_entities(self):
        """
        Retrieve the DBpedia entities found in the abstracts/titles of the CORD-19 dataset
        :return dbpedia_entities: List of Strings, list of DBpedia entities
        """
        try:
            sparql = SPARQLWrapper(self.covidOnTheWeb_endpoint)
            sparql.setQuery("""
                prefix oa: <http://www.w3.org/ns/oa#>

                select distinct (count(distinct ?entity) as ?count)
                where {
                        graph <http://ns.inria.fr/covid19/graph/dbpedia-spotlight> {
                            ?annot oa:hasBody ?entity
                        }
                }
            """)

            sparql.setReturnFormat(JSON)
            nb_entity = int(sparql.query().convert()["results"]["bindings"][0]["count"]["value"])

            print("--- Retrieve the entities.")
            with concurrent.futures.ProcessPoolExecutor() as executor:
                with tqdm.tqdm(total=ceil(nb_entity/10000)) as pbar:
                    # Workaround of virtuoso default limits
                    for dbpedia_ent_tmp in executor.map(self._dbpedia_entities_pagination, range(ceil(nb_entity / 10000))):
                        self.dbpedia_entities.extend(dbpedia_ent_tmp)
                        pbar.update()

        except Exception as err:
            traceback.print_tb(err.__traceback__)

        return self.dbpedia_entities

    def _dbpedia_entities_pagination(self, page):
        """
        Helper function used for parallelism to retrieve DBpedia entities identified in the abstracts of the CORD-19
        dataset, which bypasses Virtuoso constraints.
        :param page: page number (starting from 0), Virtuoso's limit only allows to display 10000 results
        :return: List of Strings, list of DBpedia entities
        """
        try:
            sparql = SPARQLWrapper(self.covidOnTheWeb_endpoint)
            sparql.setQuery("""
                prefix oa: <http://www.w3.org/ns/oa#>

                select distinct ?entity
                where {
                    {
                        select distinct ?entity
                        where {
                            graph <http://ns.inria.fr/covid19/graph/dbpedia-spotlight> {
                                ?annot oa:hasBody ?entity
                            }
                        } order by asc(?entity)
                    }
                } limit 10000 offset """ + str(page * 10000) + """
            """)
            sparql.setReturnFormat(JSON)
            json = sparql.query().convert()["results"]["bindings"]
            return [el["entity"]["value"] for el in json]

        except Exception as err:
            traceback.print_tb(err.__traceback__)

    def get_wikidata_entities(self):
        """
        Retrieve the Wikidata entities found in the abstracts/titles/body of the CORD-19 dataset
        :return wikidata_entities: List of Strings, list of Wikidata entities
        """
        try:
            sparql = SPARQLWrapper(self.covidOnTheWeb_endpoint)
            sparql.setQuery("""
                prefix oa: <http://www.w3.org/ns/oa#>

                select distinct (count(distinct ?entity) as ?count)
                FROM  <http://ns.inria.fr/covid19/graph/entityfishing>
                FROM <http://ns.inria.fr/covid19/graph/entityfishing/body> 
                where {
                            ?annot oa:hasBody ?entity
                }
            """)

            sparql.setReturnFormat(JSON)
            nb_entity = int(sparql.query().convert()["results"]["bindings"][0]["count"]["value"])

            print("--- Retrieve the entities.")
            with concurrent.futures.ProcessPoolExecutor() as executor:
                with tqdm.tqdm(total=ceil(nb_entity / 10000)) as pbar:
                    # Workaround of virtuoso default limits
                    for wikidata_ent_tmp in executor.map(self._wikidata_entities_pagination, range(ceil(nb_entity / 10000))):
                        self.wikidata_entities.extend(wikidata_ent_tmp)
                        pbar.update()

        except Exception as err:
            traceback.print_tb(err.__traceback__)

        return self.wikidata_entities

    def _wikidata_entities_pagination(self, page):
        """
        Helper function used for parallelism to retrieve Wikidata entities identified in the abstracts/titles/body
        of the CORD-19 dataset, which bypasses Virtuoso constraints.
        :param page: page number (starting from 0), Virtuoso's limit only allows to display 10000 results
        :return: List of Strings, list of Wikidata entities
        """
        try:
            sparql = SPARQLWrapper(self.covidOnTheWeb_endpoint)
            sparql.setQuery("""
                prefix oa: <http://www.w3.org/ns/oa#>

                select distinct ?entity
                FROM  <http://ns.inria.fr/covid19/graph/entityfishing>
                FROM <http://ns.inria.fr/covid19/graph/entityfishing/body> 
                where {
                    {
                        select distinct ?entity
                        where {
                            ?annot oa:hasBody ?entity
                        } order by asc(?entity)
                    }
                } limit 10000 offset """ + str(page * 10000) + """
            """)
            sparql.setReturnFormat(JSON)
            json = sparql.query().convert()["results"]["bindings"]
            return [el["entity"]["value"] for el in json]

        except Exception as err:
            traceback.print_tb(err.__traceback__)

    def _pico_codes_pagination(self, page):
        """
        Helper function used for parallelism to retrieve PICO elements identified in the abstracts of the CORD-19
        dataset, which bypasses Virtuoso constraints.
        :param page: page number (starting from 0), Virtuoso's limit only allows to display 10000 results
        :return: List of Strings, list of PICO elements
        """
        try:
            sparql = SPARQLWrapper(self.covidOnTheWeb_endpoint)
            sparql.setQuery("""
                prefix oa: <http://www.w3.org/ns/oa#>

                select distinct ?umls_cui
                where {
                    {
                        select distinct ?umls_cui
                        where {
                            graph <http://ns.inria.fr/covid19/graph/acta> {
                                ?annot oa:hasBody ?umls_link
                                BIND(STRAFTER(str(?umls_link), "2015AB/CUI/") as ?umls_cui)
                            }
                        } order by asc(?umls_cui)
                    }
                } limit 10000 offset """ + str(page * 10000) + """
            """)

            sparql.setReturnFormat(JSON)
            json = sparql.query().convert()["results"]["bindings"]
            return [el["umls_cui"]["value"] for el in json]

        except Exception as err:
            traceback.print_tb(err.__traceback__)

    def get_pico_codes(self):
        """
        Retrieve the PICO elements (ACTA, with UMLS CUI codes) found in the abstracts/titles of the CORD-19 dataset
        :return pico_codes: List of Strings, list of PICO elements
        """
        try:
            sparql = SPARQLWrapper(self.covidOnTheWeb_endpoint)
            sparql.setQuery("""
                prefix oa: <http://www.w3.org/ns/oa#>

                select distinct (count(distinct ?umls_cui) as ?count)
                where {
                        graph <http://ns.inria.fr/covid19/graph/acta> {
                            ?annot oa:hasBody ?umls_link
                            BIND(STRAFTER(str(?umls_link), "2015AB/CUI/") as ?umls_cui)
                        }
                }
            """)

            sparql.setReturnFormat(JSON)
            nb_entity = int(sparql.query().convert()["results"]["bindings"][0]["count"]["value"])

            print("--- Retrieve the UMLS CUI codes.")
            with concurrent.futures.ProcessPoolExecutor() as executor:
                with tqdm.tqdm(total=ceil(nb_entity / 10000)) as pbar:
                    # Workaround of virtuoso default limits
                    for pico_codes_tmp in executor.map(self._pico_codes_pagination, range(ceil(nb_entity / 10000))):
                        self.pico_codes.extend(pico_codes_tmp)
                        pbar.update()

        except Exception as err:
            traceback.print_tb(err.__traceback__)

        return self.pico_codes

    def get_links_wikidata(self, entities_list):
        """
        Retrieve the links associated to a list of Wikidata entities
        :param entities_list: List of Wikidata entities
        :return: Set with Wikidata entities as keys and their corresponding linksets as values
        """
        try:
            links = {}
            print("--- Links from Wikidata.")
            if Config.PARALLELISM is False:
                with tqdm.tqdm(total=len(entities_list)) as pbar:
                    for entity_url in entities_list:
                        links.update(self._process_links_wikidata(entity_url))
                        pbar.update()

            elif Config.PARALLELISM is True:
                with concurrent.futures.ProcessPoolExecutor() as executor:
                    with tqdm.tqdm(total=len(entities_list)) as pbar:
                        for wikidata_links_tmp in executor.map(self._process_links_wikidata, entities_list):
                            links.update(wikidata_links_tmp)
                            pbar.update()

        except Exception as err:
            traceback.print_tb(err.__traceback__)

        return links

    def _process_links_wikidata(self, entity_url):
        """
        Process used to  retrieve the links associated to a Wikidata entity
        :param entity_url: String, A Wikidata entity
        :return: Set with a Wikidata entity as key and its corresponding linksets as values
        """
        try:
            resource_links = {}
            sparql = SPARQLWrapper(self.wikidata_endpoint)
            sparql2 = SPARQLWrapper(self.dbpedia_endpoint)
            sparql.setQuery("""
                prefix wdt: <http://www.wikidata.org/prop/direct/>
                prefix wd: <http://www.wikidata.org/entity/>

                select distinct ?url_html ?url_rdf
                where {
                        <""" + entity_url + """> ?p ?o
                        BIND(URI(CONCAT("http://www.wikidata.org/entity/", STRAFTER(str(?p), "http://www.wikidata.org/prop/direct/"))) as ?property)
                        ?property wdt:P1630 ?url_html_t
                        OPTIONAL { ?property wdt:P3303 ?url_html_t }
                        OPTIONAL { ?property wdt:P1921 ?url_rdf_t }

                        BIND(REPLACE(str(?url_html_t), "\\\\$1", ?o) as ?url_html)
                        BIND(REPLACE(str(?url_rdf_t), "\\\\$1", ?o) as ?url_rdf)
                }
            """)

            sparql.setReturnFormat(JSON)
            json = sparql.query().convert()["results"]["bindings"]

            # Last one, links to RDF repositories
            resource_links = [el["url_html"]["value"] for el in json if 'url_html' in el] + \
                             [el["url_rdf"]["value"] for el in json if 'url_rdf' in el]

            # Query splitting to avoid timeouts
            sparql2.setQuery("""
                select distinct ?entity_dbpedia ?url_html ?url_html2
                where {
                        ?entity_dbpedia owl:sameAs <""" + entity_url + """>.
                        ?entity_dbpedia owl:sameAs ?url_html.
                        ?url_html2 owl:sameAs ?entity_dbpedia
                }
            """)

            sparql2.setReturnFormat(JSON)
            json = sparql2.query().convert()["results"]["bindings"]
            if len(json) > 0:
                # Restrictions here because of processing time issues with SPARQL queries (wikidata, freebase)
                resource_links += [json[0]["entity_dbpedia"]["value"]] + \
                                  [el["url_html"]["value"] for el in json if
                                   'url_html' in el and "wikidata" not in el["url_html"]["value"]
                                   and "freebase" not in el["url_html"]["value"]] + \
                                  [el["url_html2"]["value"] for el in json if
                                   'url_html2' in el and "wikidata" not in el["url_html2"]["value"]]

            resource_links = {entity_url: set(resource_links)}

        except Exception as err:
            traceback.print_tb(err.__traceback__)

        return resource_links

    def get_links_pico(self, pico_list):
        """
        Retrieve the links associated to a list of PICO elements thanks to the Wikidata SPARQL endpoint
        :param pico_list: List of PICO elements (UMLS CUI codes)
        :return: Set with UMLS entities as keys (UMLS API) and their corresponding linksets as values
        """
        try:
            links = {}
            if Config.PARALLELISM is False:
                with tqdm.tqdm(total=len(pico_list)) as pbar:
                    for umls_cui in pico_list:
                        links.update(self._process_links_pico(umls_cui))
                        pbar.update()

            elif Config.PARALLELISM is True:
                with concurrent.futures.ProcessPoolExecutor() as executor:
                    with tqdm.tqdm(total=len(pico_list)) as pbar:
                        for pico_links_tmp in executor.map(self._process_links_pico, pico_list):
                            links.update(pico_links_tmp)
                            pbar.update()

        except Exception as err:
            traceback.print_tb(err.__traceback__)

        return links

    def _process_links_pico(self, umls_cui):
        """
        Process used to retrieve the links associated to a PICO element (with UMLS CUI code) thanks to the Wikidata SPARQL endpoint
        :param umls_cui: String, An UMLS CUI codes
        :return: Set with UMLS entity as keys(UMLS API) and its corresponding linksets as values
        """
        try:
            resource_links = {}
            sparql = SPARQLWrapper(self.wikidata_endpoint)
            sparql2 = SPARQLWrapper(self.dbpedia_endpoint)
            sparql.setQuery("""
                prefix wdt: <http://www.wikidata.org/prop/direct/>
                prefix wd: <http://www.wikidata.org/entity/>
                
                select distinct ?url_html ?url_rdf ?entity_wikidata
                where {
                        ?entity_wikidata wdt:P2892 \"""" + umls_cui + """\" .
                        ?entity_wikidata ?p ?o
                        BIND(URI(CONCAT("http://www.wikidata.org/entity/", STRAFTER(str(?p), "http://www.wikidata.org/prop/direct/"))) as ?property)
                        ?property wdt:P1630 ?url_html_t
                        OPTIONAL { ?property wdt:P3303 ?url_html_t }
                        OPTIONAL { ?property wdt:P1921 ?url_rdf_t }
    
                        BIND(REPLACE(str(?url_html_t), "\\\\$1", ?o) as ?url_html)
                        BIND(REPLACE(str(?url_rdf_t), "\\\\$1", ?o) as ?url_rdf)
                }
            """)

            sparql.setReturnFormat(JSON)
            json = sparql.query().convert()["results"]["bindings"]

            # No resource found with this UMLS code in wikidata
            if len(json) > 0:
                # Middle one, links to RDF repositories
                entity_wikidata = json[0]["entity_wikidata"]["value"]
                resource_links = [el["url_html"]["value"] for el in json if 'url_html' in el] + \
                                 [el["url_rdf"]["value"] for el in json if 'url_rdf' in el] + \
                                 [entity_wikidata]

                # Query splitting to avoid timeouts
                sparql2.setQuery("""
                                   select distinct ?entity_dbpedia ?url_html ?url_html2
                                   where {
                                        ?entity_dbpedia owl:sameAs <""" + entity_wikidata + """>.
                                        ?entity_dbpedia owl:sameAs ?url_html.
                                        ?url_html2 owl:sameAs ?entity_dbpedia
                                   }
                               """)

                sparql2.setReturnFormat(JSON)
                json = sparql2.query().convert()["results"]["bindings"]
                if len(json) > 0:
                    # Restrictions here because of processing time issues with SPARQL queries (wikidata, freebase)
                    resource_links += [json[0]["entity_dbpedia"]["value"]] + \
                                      [el["url_html"]["value"] for el in json if
                                       'url_html' in el and "wikidata" not in el["url_html"]["value"]
                                       and "freebase" not in el["url_html"]["value"]] + \
                                      [el["url_html2"]["value"] for el in json if
                                       'url_html2' in el and "wikidata" not in el["url_html2"]["value"]]
                resource_links = {Config.umls_namespace + umls_cui: set(resource_links)}

        except Exception as err:
            resource_links = {Config.umls_namespace + umls_cui: set(resource_links)}
            traceback.print_tb(err.__traceback__)

        return resource_links

    def get_links_dbpedia(self, entities_list):
        """
        Retrieve the links associated to a list of DBpedia entities
        :param entities_list: List of Strings, list of DBpedia entities
        :return: Set with DBpedia entities as keys and their corresponding linksets as values
        """
        try:
            links = {}
            if Config.PARALLELISM is False:
                with tqdm.tqdm(total=len(entities_list)) as pbar:
                    for entity_url in entities_list:
                        links.update(self._process_links_dbpedia(entity_url))
                        pbar.update()

            elif Config.PARALLELISM is True:
                with concurrent.futures.ProcessPoolExecutor() as executor:
                    with tqdm.tqdm(total=len(entities_list)) as pbar:
                        for dbpedia_links_tmp in executor.map(self._process_links_dbpedia, entities_list):
                            links.update(dbpedia_links_tmp)
                            pbar.update()

        except Exception as err:
            traceback.print_tb(err.__traceback__)

        return links

    def _process_links_dbpedia(self, entity_url):
        """
        Process used to retrieve the links associated to a DBpedia entity
        :param entity_url: String, A DBpedia entity
        :return: Set with a DBpedia entity as key and its corresponding linksets as values
        """
        try:
            resource_links = {}
            sparql = SPARQLWrapper(self.dbpedia_endpoint)
            sparql2 = SPARQLWrapper(self.wikidata_endpoint)
            sparql.setQuery("""
                       select distinct ?url_html
                       where {
                               {
                                   <""" + entity_url + """> owl:sameAs ?url_html
                               } union {
                                   ?url_html owl:sameAs <""" + entity_url + """>
                               }
                               FILTER(!CONTAINS(str(?url_html), "wikidata.dbpedia") )
                               FILTER(!CONTAINS(str(?url_html), "freebase") )
                       }
                   """)
            sparql.setReturnFormat(JSON)
            json = sparql.query().convert()["results"]["bindings"]
            # Last one, links to RDF repositories
            resource_links = [el["url_html"]["value"] for el in json if 'url_html' in el]
            wikidata_entity = next((s for s in resource_links if "http://www.wikidata.org/entity/" in s), None)

            if wikidata_entity:
                # Query splitting to avoid timeouts
                sparql2.setQuery("""
                           prefix wdt: <http://www.wikidata.org/prop/direct/>
                           prefix wd: <http://www.wikidata.org/entity/>

                           select distinct ?url_html ?url_rdf
                           where {
                                   <""" + wikidata_entity + """> ?p ?o
                                   BIND(URI(CONCAT("http://www.wikidata.org/entity/", STRAFTER(str(?p), "http://www.wikidata.org/prop/direct/"))) as ?property)
                                   ?property wdt:P1630 ?url_html_t
                                   OPTIONAL { ?property wdt:P3303 ?url_html_t }
                                   OPTIONAL { ?property wdt:P1921 ?url_rdf_t }

                                   BIND(REPLACE(str(?url_html_t), "\\\\$1", ?o) as ?url_html)
                                   BIND(REPLACE(str(?url_rdf_t), "\\\\$1", ?o) as ?url_rdf)
                           }
                       """)

                sparql2.setReturnFormat(JSON)
                json = sparql2.query().convert()["results"]["bindings"]
                # Last one, links to RDF repositories
                resource_links += [el["url_html"]["value"] for el in json if 'url_html' in el] + \
                                  [el["url_rdf"]["value"] for el in json if 'url_rdf' in el]

            resource_links = {entity_url: set(resource_links)}

        except Exception as err:
            traceback.print_tb(err.__traceback__)

        return resource_links


class Wrapper(object):

    def request_ncbo_with_cui(self, pico_list, api_key=Config.ncbo_api_key):
        """
        Retrieve the links associated to a list of PICO elements thanks to the BioPortal API
        :param pico_list: List of Strings, list of PICO elements (UMLS CUI codes)
        :param api_key: String, API key to access the NCBO API Web Service
        :return: dict with UMLS entities as keys (UMLS API) and their corresponding linksets as values
        """
        try:
            links = {}
            with concurrent.futures.ProcessPoolExecutor() as executor:
                with tqdm.tqdm(total=len(pico_list)) as pbar:
                    ncbo_request = { executor.submit(self._process_ncbo_request, cui, api_key): cui for cui in pico_list }
                    for future in concurrent.futures.as_completed(ncbo_request):
                        links.update(future.result())
                        pbar.update()
            return links

        except Exception as err:
            traceback.print_tb(err.__traceback__)

    def _process_ncbo_request(self, cui, api_key=Config.ncbo_api_key):
        """
        Process used to retrieve the links associated to a PICO element thanks to the BioPortal API
        :param cui: String, UMLS CUI code
        :param api_key: String, API key to access the NCBO API Web Service
        :return: Dict with UMLS entities as keys (UMLS API) and their corresponding linksets as values
        """
        try:
            params = {
                'apikey': api_key,
                'cui': cui,
            }

            response = requests.get("http://data.bioontology.org/search", params=params)
            raw = json.loads(str(response.text))

            direct_resources = [x["@id"] for x in raw["collection"]]
            mappings = [x["links"]["mappings"] for x in raw["collection"]]

            # Timeout with the code below
            # resource_links = self.resquest_ncbo_mapping(mappings) + direct_resources
            resource_links = direct_resources
            resource_links = { Config.umls_namespace + cui: set(resource_links) }
            return resource_links

        except Exception as err:
            traceback.print_tb(err.__traceback__)

    def _process_ncbo_mapping(self, url, api_key=Config.ncbo_api_key):
        """
        Process used to retrieve the links from a mapping URL of the BioPortal API
        :param url: String, mapping URL comming from BioPortal
        :param api_key: String, API key to access the NCBO API Web Service
        :return: List, list of links or empty list
        """
        try:
            params = {
                'apikey': api_key,
            }

            response = requests.get(url, params=params)
            # Issue with null type
            raw = json.loads(str(response.text))
            # Too many requests or not found
            if "errors" in raw:
                uri = []
            else:
                uri = [x["@id"] for y in raw for x in y["classes"]]
            return uri

        except Exception as err:
            traceback.print_tb(err.__traceback__)

    def resquest_ncbo_mapping(self, url_list, api_key=Config.ncbo_api_key):
        """
        Retrieve the links found in the mapping URLs of the BioPortal API
        :param url_list: List of Strings, URLs which propose a mapping to other ontologies
        :param api_key: String, API key to access the NCBO API Web Service
        :return: List, list of links
        """
        try:
            mapped_links = []
            with concurrent.futures.ProcessPoolExecutor() as executor:
                ncbo_mapping = { executor.submit(self._process_ncbo_mapping, url, api_key): url for url in url_list }
                for future in concurrent.futures.as_completed(ncbo_mapping):
                    mapped_links += future.result()

            return list(set(mapped_links))

        except Exception as err:
            traceback.print_tb(err.__traceback__)
