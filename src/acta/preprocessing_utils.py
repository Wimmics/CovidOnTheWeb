import os
import json

def get_text(data, section="abstract", minlength=10):
    '''
    Gets text field from a
    :param data: bytestream
    :param section: json key for target section
    :param minlength: minimum threshold to consider text
    :return: string with text
    '''
    json_obj = json.loads(data)
    section = json_obj[section]
    paper_id = json_obj["paper_id"]

    if len(section) < 1:
        return None, paper_id
    else:
        abstr_text = []
        for i, _ in enumerate(section):

            text = section[i]["text"]
            abstr_text.append(text)

        abstr_text = ' '.join(abstr_text)
        if len(abstr_text.split()) < minlength:
            return None, paper_id

        return abstr_text, paper_id

def get_abstracts(folder, minlength=10):
    '''
    Gets the text from the abstract section for every file in a folder.
    :param folder: path to data folder
    :param minlength: minimum threshold to consider text
    :return:
    '''
    files = os.listdir(folder)
    abstracts = {}
    for file_name in files:
        file_path = os.path.join(folder, file_name)
        with open(file_path) as f:
            data = f.read()
            text = get_text(data, "abstract", minlength)
            if text:
                abstracts[file_name] = text
    return abstracts

def tokenize_sentences(text):
    from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters, PunktLanguageVars
    class CommaPoint(PunktLanguageVars):
        sent_end_chars = ('.', '?', '!')

    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'al', 'i.v'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param, lang_vars=CommaPoint())
    sentences = sentence_splitter.tokenize(text)

    return sentences
