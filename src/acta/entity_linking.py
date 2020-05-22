import os
import json
import spacy
import scispacy
from tqdm import tqdm
from scispacy.umls_linking import UmlsEntityLinker
from scispacy.abbreviation import AbbreviationDetector


def aggregate_json(pipeline, fin_path):
    """
    Links each intervention, outcome and participant entry in a json file to UMLS concepts.
    :param pipeline: ScispaCy pipeline
    :param fin_path: path to folder with input files (json format)
    """

    with open(os.path.join(os.getcwd(), fin_path)) as fin:
        data = json.load(fin)
        for i, c in enumerate(data["components"]):
            if 'outcome' in c.keys():
                for o in c["outcome"]:
                    doc = pipeline(o["text"])
                    entities = doc.ents
                    ents = []
                    for entity in entities:
                        for umls_ent in entity._.umls_ents:
                            tmp = {}
                            cui, prob = umls_ent
                            results = linker.umls.cui_to_entity[umls_ent[0]]
                            tmp["name"] = str(entity)
                            tmp["concept_id"] = results.concept_id
                            tmp["confidence"] = str(round(prob, 2))
                            tmp["canonical_name"] = results.canonical_name
                            tmp["tui"] = results.types
                            ents.append(tmp)
                    if ents != []:
                        o["linked_to"] = ents
            if 'intervention' in c.keys():
                for o in c["intervention"]:
                    doc = pipeline(o["text"])
                    entities = doc.ents
                    ents = []
                    for entity in entities:
                        for umls_ent in entity._.umls_ents:
                            tmp = {}
                            cui, prob = umls_ent
                            results = linker.umls.cui_to_entity[umls_ent[0]]
                            tmp["name"] = str(entity)
                            tmp["concept_id"] = results.concept_id
                            tmp["confidence"] = str(round(prob, 2))
                            tmp["canonical_name"] = results.canonical_name
                            tmp["tui"] = results.types
                            ents.append(tmp)
                    if ents != []:
                        o["linked_to"] = ents
            if 'participants' in c.keys():
                for o in c["participants"]:
                    doc = pipeline(o["text"])
                    entities = doc.ents
                    ents = []
                    for entity in entities:
                        for umls_ent in entity._.umls_ents:
                            tmp = {}
                            cui, prob = umls_ent
                            results = linker.umls.cui_to_entity[umls_ent[0]]
                            tmp["name"] = str(entity)
                            tmp["concept_id"] = results.concept_id
                            tmp["confidence"] = str(round(prob, 2))
                            tmp["canonical_name"] = results.canonical_name
                            tmp["tui"] = results.types
                            ents.append(tmp)
                    if ents != []:
                        o["linked_to"] = ents

    #import pprint as pp
    #pp.pprint(data)

    with open(os.path.join(os.getcwd(), fin_path), "w") as fout:
        fout.write(json.dumps(data))



# load pre-trained model
nlp = spacy.load("en_core_sci_sm")

# for details see https://github.com/allenai/scispacy
#abbreviation_pipe = AbbreviationDetector(nlp)
#nlp.add_pipe(abbreviation_pipe)

linker = UmlsEntityLinker(resolve_abbreviations=True, threshold=0.8)
nlp.add_pipe(linker)

# run pipeline in folder
data_dir = "./output/"
files = os.listdir(os.path.join(os.getcwd(), data_dir))
for f in tqdm(files):
    aggregate_json(nlp, os.path.join(data_dir, f))
