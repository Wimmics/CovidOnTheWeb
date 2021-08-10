import concurrent.futures
import os
import pathlib
import traceback

import cotools
import tqdm
import pycld2

from cord19_ner.utils.config import Config
from cord19_ner.utils.iodata import Output
from cord19_ner.wrapper.wrapper_annotator import WrapperAnnotator


def func_entity_fishing(d):
    """
    Helper function for processing a paper in a thread with Entity-fishing
    :param d: content of the paper
    :return: result of the annotation with Entity-fishing in JSON || None if the JSON annotation exists already
    """
    d_json = {}
    paper_id = d['paper_id']
    title = d["metadata"]["title"]
    if os.path.isfile(path_output + '/entity-fishing/' + folder + '/' + paper_id + '.json'):
        pbar.update()
        return None
    try:
        body_text = cotools.text(d)
        isreliable, textbytesfound, details, vectors = pycld2.detect(body_text, returnVectors=True)
        lang = vectors[0][3]
    # None or out of range
    except Exception:
        lang = 'en'

    d_json["paper_id"] = paper_id
    d_json["lang"] = lang
    try:
        abstract = cotools.abstract(d)
        d_json["abstract"] = wa.request_entity_fishing(abstract, lang)
    # no abstract
    except Exception:
        pass

    d_json["title"] = wa.request_entity_fishing(title, lang)
    d_json["body_text"] = wa.request_entity_fishing(body_text, lang)

    d_json["ref_entries"] = {}
    for key, value in d["ref_entries"].items():
        d_json["ref_entries"][key] = wa.request_entity_fishing(value["text"])

    # d_json["bib_entries"] = {}
    # for key, value in d["bib_entries"].items():
    #    d_json["bib_entries"][key] = wa.request_entity_fishing(value["title"])

    d_json["back_matter"] = []
    for matter in d["back_matter"]:
        for key, value in matter.items():
            if key == 'text':
                text = {'text': wa.request_entity_fishing(value)}
                d_json["back_matter"].append(text)

    Output().save_json(d_json, path_output + '/entity-fishing/' + folder + '/' + d["paper_id"] +  '.json')
    pbar.update()
    return d_json


def func_dbpedia_spotlight(d):
    """
    Helper function for processing a paper in a thread with DBpedia Spotlight
    :param d: content of the paper
    :return: result of the annotation with DBpedia Spotlight in JSON || None if the JSON annotation exists already
    """
    d_json = {}
    paper_id = d['paper_id']
    title = d["metadata"]["title"]
    if os.path.isfile(path_output + '/dbpedia-spotlight/' + folder + '/' + paper_id + '.json'):
        pbar.update()
        return None
    try:
        body_text = cotools.text(d)
        isreliable, textbytesfound, details, vectors = pycld2.detect(body_text, returnVectors=True)
        lang = vectors[0][3]
    # None or out of range
    except:
        lang = 'en'

    if os.path.isfile('/data/CORD19-Annotation-multi/entity-fishing/' + folder + '/' + paper_id + '.json'):
        return None

    d_json["paper_id"] = paper_id
    d_json["lang"] = lang
    try:
        abstract = cotools.abstract(d)
        d_json["abstract"] = wa.request_dbpedia_spotlight(abstract, lang)
    # no abstract
    except Exception:
        pass

    d_json["title"] = wa.request_dbpedia_spotlight(title, lang)
    d_json["body_text"] = wa.request_dbpedia_spotlight(body_text, lang)

    d_json["ref_entries"] = {}
    for key, value in d["ref_entries"].items():
        d_json["ref_entries"][key] = wa.request_dbpedia_spotlight(value["text"])

    #d_json["bib_entries"] = {}
    #for key, value in d["bib_entries"].items():
    #    d_json["bib_entries"][key] = wa.request_dbpedia_spotlight(value["title"])

    d_json["back_matter"] = []
    for matter in d["back_matter"]:
        for key, value in matter.items():
            if key == 'text':
                text = {'text': wa.request_dbpedia_spotlight(value)}
                d_json["back_matter"].append(text)

    Output().save_json(d_json, path_output + '/dbpedia-spotlight/' + folder + '/' + d["paper_id"] + '.json')
    pbar.update()
    return d_json


def func_ncbo(d):
    """
    Helper function for processing a paper in a thread with NCBO BioPortal Annotator+
    :param d: content of the paper
    :return: result of the annotation with NCBO BioPortal Annotator+ in JSON ||
     None if the JSON annotation exists already
    """
    d_json = {}
    paper_id = d['paper_id']
    title = d["metadata"]["title"]
    if os.path.isfile(path_output + '/ncbo/' + folder + '/' + paper_id + '.json'):
        return None

    try:
        body_text = cotools.text(d)
        isreliable, textbytesfound, details, vectors = pycld2.detect(body_text, returnVectors=True)
        lang = vectors[0][3]
    # None or out of range
    except Exception:
        lang = 'en'

    if os.path.isfile('/data/CORD19-Annotation-multi/entity-fishing/' + folder + '/' + paper_id + '.json'):
        return None

    d_json["paper_id"] = paper_id
    d_json["lang"] = lang
    try:
        abstract = cotools.abstract(d)
        d_json["abstract"] = wa.request_ncbo_plus(abstract, lang)
    # no abstract
    except Exception:
        pass

    body_text = cotools.text(d)

    d_json["paper_id"] = paper_id
    d_json["title"] = wa.request_ncbo_plus(title, lang)
    d_json["body_text"] = wa.request_ncbo_plus(body_text, lang)
    d_json["ref_entries"] = {}
    for key, value in d["ref_entries"].items():
        d_json["ref_entries"][key] = wa.request_ncbo_plus(value["text"], lang)

    d_json["back_matter"] = []
    for matter in d["back_matter"]:
        for key, value in matter.items():
            if key == 'text':
                text = {'text': wa.request_ncbo_plus(value)}
                d_json["back_matter"].append(text)
    pbar.update()
    Output().save_json(d_json, path_output + '/ncbo/' + folder + '/' + d["paper_id"] + '.json')
    return d_json


if __name__ == '__main__':
    # Path to the CORD-19 dataset
    project_resources = Config.project_resources
    # Path where the annotated files will be saved
    path_output = Config.corpus_annotated
    pathlib.Path(os.path.dirname(project_resources)).mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.dirname(path_output)).mkdir(parents=True, exist_ok=True)
    if Config.DOWNLOAD_CORPUS:
        cotools.download(dir=project_resources)
    wa = WrapperAnnotator()
    folders_corpus = ["pdf_json", "pmc_json"]

    for folder in folders_corpus:
        data = cotools.Paperset(project_resources + '/' + folder)

        # You may want to change the number of workers
        if Config.ENTITY_FISHING:
            with tqdm.tqdm(total=len(data)) as pbar:
                with concurrent.futures.ProcessPoolExecutor() as executor:
                    executor.map(func_entity_fishing, data)

        if Config.DBPEDIA_SPOTLIGHT:
            with tqdm.tqdm(total=len(data)) as pbar:
                with concurrent.futures.ProcessPoolExecutor() as executor:
                    executor.map(func_dbpedia_spotlight, data)

        if Config.NCBO_BIOPORTAL:
            with tqdm.tqdm(total=len(data)) as pbar:
                with concurrent.futures.ProcessPoolExecutor() as executor:
                    executor.map(func_ncbo, data)
