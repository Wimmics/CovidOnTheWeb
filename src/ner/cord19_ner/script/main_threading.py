import concurrent.futures
import cotools
import os
import pathlib
import tqdm

from cord19_ner.utils.config import Config
from cord19_ner.utils.iodata import Output
from cord19_ner.wrapper.wrapper_annotator import WrapperAnnotator

DOWNLOAD_CORPUS = False

# Options to run NER tools
DBPEDIA_SPOTLIGHT = False
ENTITY_FISHING = False
NCBO_BIOPORTAL = False


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
        return None
    try:
        abstract = cotools.abstract(d)
        d_json["abstract"] = wa.request_entity_fishing(abstract)
    # no abstract
    except:
        pass
    body_text = cotools.text(d)

    d_json["paper_id"] = paper_id
    d_json["title"] = wa.request_entity_fishing(title)
    d_json["body_text"] = wa.request_entity_fishing(body_text)

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
        return None
    try:
        abstract = cotools.abstract(d)
        d_json["abstract"] = wa.request_dbpedia_spotlight(abstract)
    # no abstract
    except:
        pass
    body_text = cotools.text(d)

    d_json["paper_id"] = paper_id
    d_json["title"] = wa.request_dbpedia_spotlight(title)
    d_json["body_text"] = wa.request_dbpedia_spotlight(body_text)

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
        abstract = cotools.abstract(d)
        d_json["abstract"] = wa.request_ncbo_plus(abstract)
    # no abstract
    except:
        pass

    body_text = cotools.text(d)

    d_json["paper_id"] = paper_id
    d_json["title"] = wa.request_ncbo_plus(title)
    """
    d_json["body_text"] = wa.request_ncbo_plus(body_text)
    #time.sleep(15)
    d_json["ref_entries"] = {}
    for key, value in d["ref_entries"].items():
        d_json["ref_entries"][key] = wa.request_ncbo_plus(value["text"])

    #d_json["bib_entries"] = {}
    #for key, value in d["bib_entries"].items():
    #    d_json["bib_entries"][key] = wa.request_ncbo_plus(value["title"])

    d_json["back_matter"] = []
    for matter in d["back_matter"]:
        for key, value in matter.items():
            if key == 'text':
                text = {'text': wa.request_ncbo_plus(value)}
                d_json["back_matter"].append(text)
    """
    return d_json


if __name__ == '__main__':
    # Path to the CORD-19 dataset
    project_resources = Config.project_resources
    # Path where the annotated files will be saved
    path_output = Config.corpus_annotated
    pathlib.Path(os.path.dirname(project_resources)).mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.dirname(path_output)).mkdir(parents=True, exist_ok=True)
    if DOWNLOAD_CORPUS:
        cotools.download(dir=project_resources)
    wa = WrapperAnnotator()
    folders_corpus = ["biorxiv_medrxiv/pdf_json", "comm_use_subset/pdf_json", "comm_use_subset/pmc_json",
                      "noncomm_use_subset/pdf_json", "noncomm_use_subset/pmc_json", "custom_license/pdf_json",
                      "custom_license/pmc_json"]
    for folder in folders_corpus:
        data = cotools.Paperset(project_resources + '/' + folder)

        # You may want to change the number of workers
        with concurrent.futures.ProcessPoolExecutor() as executor:
            if ENTITY_FISHING:
                with tqdm.tqdm(total=len(data)) as pbar:
                    for d in executor.map(func_entity_fishing, data):
                        if d is not None:
                            Output().save_json(d, path_output + '/entity-fishing/' + folder + '/' + d["paper_id"] +
                                               '.json')
                        del d
                        pbar.update()
                #shutil.make_archive(path_output + '/' + folder, 'zip', path_output + '/' + folder)

            if DBPEDIA_SPOTLIGHT:
                with tqdm.tqdm(total=len(data)) as pbar:
                    for d in executor.map(func_dbpedia_spotlight, data):
                        if d is not None:
                            Output().save_json(d, path_output + '/dbpedia-spotlight/' + folder + '/' + d["paper_id"] +
                                               '.json')
                        del d
                        pbar.update()
                #shutil.make_archive(path_output + '/' + folder, 'zip', path_output + '/' + folder)

            if NCBO_BIOPORTAL:
                with tqdm.tqdm(total=len(data)) as pbar:
                    for d in executor.map(func_ncbo, data):
                        if d is not None:
                            Output().save_json(d, path_output + '/ncbo/' + folder + '/' + d["paper_id"] + '.json')
                        del d
                        pbar.update()
                #shutil.make_archive(path_output + '/' + folder, 'zip', path_output + '/' + folder)
