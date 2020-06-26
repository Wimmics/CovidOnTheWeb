import traceback

from SPARQLWrapper import SPARQLWrapper, JSON

from covidontheweb_aug.utils.config import Config

class KnowledgeGraphRequest(object):
    # TODO handle BioPartal entities
    def __init__(self):
        # Endpoints
        self.corese_endpoint = Config.corese_endpoint
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
            sparql = SPARQLWrapper(self.corese_endpoint)
            sparql.setQuery("""
                prefix oa: <http://www.w3.org/ns/oa#>

                select distinct ?entity
                where {
                    SERVICE <""" + self.covidOnTheWeb_endpoint + """> { 
                        graph <http://ns.inria.fr/covid19/graph/dbpedia-spotlight> {
                            ?annot oa:hasBody ?entity
                        }
                    }
                }
            """)

            sparql.setReturnFormat(JSON)
            json = sparql.query().convert()["results"]["bindings"]
            self.dbpedia_entities = [el["entity"]["value"] for el in json]
        except Exception as err:
            traceback.print_tb(err.__traceback__)

        return self.dbpedia_entities

    def get_wikidata_entities(self):
        """
        Retrieve the Wikidata entities found in the abstracts/titles of the CORD-19 dataset
        :return wikidata_entities: List of Strings, list of Wikidata entities
        """
        try:
            sparql = SPARQLWrapper(self.corese_endpoint)
            sparql.setQuery("""
                prefix oa: <http://www.w3.org/ns/oa#>
                
                select distinct ?entity
                where {
                    SERVICE <""" + self.covidOnTheWeb_endpoint + """> { 
                        graph <http://ns.inria.fr/covid19/graph/entityfishing> {
                            ?annot oa:hasBody ?entity
                        }
                        
                        # Server unable to return entities on bodies at the moment.
                        # graph <http://ns.inria.fr/covid19/graph/entityfishing/body> {
                        #    ?annot oa:hasBody ?entity
                        # }
                    }
                }
            """)

            sparql.setReturnFormat(JSON)
            json = sparql.query().convert()["results"]["bindings"]
            self.wikidata_entities = [el["entity"]["value"] for el in json]
        except Exception as err:
            traceback.print_tb(err.__traceback__)

        return self.wikidata_entities

    def get_pico_codes(self):
        """
        Retrieve the PICO elements (ACTA, with UMLS CUI codes) found in the abstracts/titles of the CORD-19 dataset
        :return pico_codes: List of Strings, list of PICO elements
        """
        try:
            sparql = SPARQLWrapper(self.corese_endpoint)
            sparql.setQuery("""
                prefix oa: <http://www.w3.org/ns/oa#>

                select distinct ?umls_cui
                where {
                    SERVICE <""" + self.covidOnTheWeb_endpoint + """> { 
                        graph <http://ns.inria.fr/covid19/graph/acta> {
                            ?annot oa:hasBody ?umls_link
                            BIND(STRAFTER(str(?umls_link), "2015AB/CUI/") as ?umls_cui)
                        }
                    }
                }
            """)

            sparql.setReturnFormat(JSON)
            json = sparql.query().convert()["results"]["bindings"]
            self.pico_codes = [el["umls_cui"]["value"] for el in json]
        except Exception as err:
            traceback.print_tb(err.__traceback__)

        return self.pico_codes

    def get_links_wikidata(self, entities_list):
        """
        Retrieve the links associated to a list of Wikidata entities
        :param entities_list: List of Wikidata entities
        :return: Set with Wikidata entities as keys and their corresponding resources as values
        """
        try:
            links = {}
            sparql = SPARQLWrapper(self.corese_endpoint)
            # TODO parallelize query, watch out for timeouts
            for entity_url in entities_list:
                sparql.setQuery("""
                    prefix wdt: <http://www.wikidata.org/prop/direct/>
                    prefix wd: <http://www.wikidata.org/entity/>
                    
                    select distinct ?url_html ?url_rdf
                    where {
                        SERVICE <""" + self.wikidata_endpoint + """> {
                            <""" + entity_url + """> ?p ?o
                            BIND(URI(CONCAT("http://www.wikidata.org/entity/", STRAFTER(str(?p), "http://www.wikidata.org/prop/direct/"))) as ?property)
                            ?property wdt:P1630 ?url_html_t
                            OPTIONAL { ?property wdt:P3303 ?url_html_t }
                            OPTIONAL { ?property wdt:P1921 ?url_rdf_t }
                            
                            BIND(REPLACE(str(?url_html_t), "\\\\$1", ?o) as ?url_html)
                            BIND(REPLACE(str(?url_rdf_t), "\\\\$1", ?o) as ?url_rdf)
                        }
                    }
                """)

                sparql.setReturnFormat(JSON)
                json = sparql.query().convert()["results"]["bindings"]

                # Last one, links to RDF repositories
                resource_links = [el["url_html"]["value"] for el in json if 'url_html' in el] + \
                             [el["url_rdf"]["value"] for el in json if 'url_rdf' in el]


                # Query splitting to avoid timeouts
                sparql.setQuery("""
                    select distinct ?entity_dbpedia ?url_html
                    where {
                        SERVICE <""" + self.dbpedia_endpoint + """> {
                            ?entity_dbpedia owl:sameAs <""" + entity_url + """>
                            ?entity_dbpedia owl:sameAs ?url_html
                            
                            FILTER(!CONTAINS(str(?url_html), "wikidata"))
                            FILTER(!CONTAINS(str(?url_html), "freebase") )
                        }
                    }
                """)

                sparql.setReturnFormat(JSON)
                json = sparql.query().convert()["results"]["bindings"]
                if len(json) > 0:
                    resource_links += [json[0]["entity_dbpedia"]["value"]] + \
                        [el["url_html"]["value"] for el in json if 'url_html' in el]

                resource_links = { entity_url: set(resource_links) }

                links.update(resource_links)
        except Exception as err:
            traceback.print_tb(err.__traceback__)

        return links

    def get_links_pico(self, pico_list):
        """
        Retrieve the links associated to a list of PICO elements
        :param pico_list: List of PICO elements (UMLS CUI codes)
        :return: Set with UMLS entities as keys (UMLS API) and their corresponding resources as values
        """
        try:
            links = {}
            sparql = SPARQLWrapper(self.corese_endpoint)
            # TODO parallelize query, watch out for timeouts
            for umls_cui in pico_list:
                sparql.setQuery("""
                    prefix wdt: <http://www.wikidata.org/prop/direct/>
                    prefix wd: <http://www.wikidata.org/entity/>

                    select distinct ?url_html ?url_rdf ?entity_wikidata
                    where {
                        SERVICE <https://query.wikidata.org/sparql> {
                            ?entity_wikidata wdt:P2892 \"""" + umls_cui + """\" .
                            ?entity_wikidata ?p ?o
                            BIND(URI(CONCAT("http://www.wikidata.org/entity/", STRAFTER(str(?p), "http://www.wikidata.org/prop/direct/"))) as ?property)
                            ?property wdt:P1630 ?url_html_t
                            OPTIONAL { ?property wdt:P3303 ?url_html_t }
                            OPTIONAL { ?property wdt:P1921 ?url_rdf_t }

                            BIND(REPLACE(str(?url_html_t), "\\\\$1", ?o) as ?url_html)
                            BIND(REPLACE(str(?url_rdf_t), "\\\\$1", ?o) as ?url_rdf)
                        }
                    }
                """)

                sparql.setReturnFormat(JSON)
                json = sparql.query().convert()["results"]["bindings"]

                # No resource found with this UMLS code in wikidata
                if len(json) > 0:
                    # Last one, links to RDF repositories
                    entity_wikidata = json[0]["entity_wikidata"]["value"]
                    resource_links = [el["url_html"]["value"] for el in json if 'url_html' in el] + \
                                     [el["url_rdf"]["value"] for el in json if 'url_rdf' in el] + \
                                     [entity_wikidata]

                    # Query splitting to avoid timeouts
                    sparql.setQuery("""
                                       select distinct ?entity_dbpedia ?url_html
                                       where {
                                           SERVICE <""" + self.dbpedia_endpoint + """> {
                                               ?entity_dbpedia owl:sameAs <""" + entity_wikidata + """>
                                               ?entity_dbpedia owl:sameAs ?url_html


                                               BIND(STRAFTER(\"""" + entity_wikidata + """\", "entity/") as ?wikidata_code)

                                               FILTER(!CONTAINS(str(?url_html), "wikidata"))
                                               FILTER(!CONTAINS(str(?url_html), "freebase") )
                                           }
                                       }
                                   """)

                    sparql.setReturnFormat(JSON)
                    json = sparql.query().convert()["results"]["bindings"]
                    if len(json) > 0:
                        resource_links += [json[0]["entity_dbpedia"]["value"]] + \
                                          [el["url_html"]["value"] for el in json if 'url_html' in el]

                    resource_links = {"https://uts-ws.nlm.nih.gov/rest/semantic-network/2015AB/CUI/" +
                                      umls_cui: set(resource_links)}

                    links.update(resource_links)

        except Exception as err:
            traceback.print_tb(err.__traceback__)
        return links


    def get_links_dbpedia(self, entities_list):
        """
        Retrieve the links associated to a list of DBpedia entities
        :param entities_list: List of DBpedia entities
        :return: Set with DBpedia entities as keys and their corresponding resources as values
        """
        try:
            links = {}
            sparql = SPARQLWrapper(self.corese_endpoint)
            # TODO parallelize query, watch out for timeouts
            for entity_url in entities_list:
                sparql.setQuery("""
                        select distinct ?url_html
                        where {
                            SERVICE <""" + self.dbpedia_endpoint + """> {
                                <""" + entity_url + """> owl:sameAs ?url_html
                                
                                FILTER(!CONTAINS(str(?url_html), "wikidata.dbpedia") )
                                FILTER(!CONTAINS(str(?url_html), "freebase") )
                            }
                        }
                    """)

                sparql.setReturnFormat(JSON)
                json = sparql.query().convert()["results"]["bindings"]

                # Last one, links to RDF repositories
                resource_links = [el["url_html"]["value"] for el in json if 'url_html' in el]
                wikidata_entity = next((s for s in resource_links if "http://www.wikidata.org/entity/" in s), None)

                if wikidata_entity:
                    # Query splitting to avoid timeouts
                    sparql.setQuery("""
                            prefix wdt: <http://www.wikidata.org/prop/direct/>
                            prefix wd: <http://www.wikidata.org/entity/>
                            
                            select distinct ?url_html ?url_rdf
                            where {
                                SERVICE <""" + self.wikidata_endpoint + """> {
                                    <""" + wikidata_entity + """> ?p ?o
                                    BIND(URI(CONCAT("http://www.wikidata.org/entity/", STRAFTER(str(?p), "http://www.wikidata.org/prop/direct/"))) as ?property)
                                    ?property wdt:P1630 ?url_html_t
                                    OPTIONAL { ?property wdt:P3303 ?url_html_t }
                                    OPTIONAL { ?property wdt:P1921 ?url_rdf_t }
                                    
                                    BIND(REPLACE(str(?url_html_t), "\\\\$1", ?o) as ?url_html)
                                    BIND(REPLACE(str(?url_rdf_t), "\\\\$1", ?o) as ?url_rdf)
                                }
                            }
                        """)

                    sparql.setReturnFormat(JSON)
                    json = sparql.query().convert()["results"]["bindings"]
                    # Last one, links to RDF repositories
                    resource_links += [el["url_html"]["value"] for el in json if 'url_html' in el] + \
                                 [el["url_rdf"]["value"] for el in json if 'url_rdf' in el]

                resource_links = {entity_url: set(resource_links)}

                links.update(resource_links)

        except Exception as err:
            traceback.print_tb(err.__traceback__)

        return links
