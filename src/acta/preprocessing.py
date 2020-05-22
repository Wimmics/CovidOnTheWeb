import json
import os
from tqdm import tqdm
from preprocessing_utils import get_text

base_dir = './data/v7/'


def check_for_abstract(data):
    """
    Checks if JSON has 'abstract' as a key.
    :param data: data stream
    """
    def _recursion(dictionary):
        if type(dictionary) is not dict:
            return False
        if 'abstract' in dictionary.keys():
            return True
        for key in dictionary.keys():
            if type(dictionary[key]) is dict:
                _recursion(dictionary[key])
    json_obj = json.loads(data)
    paper_id = json_obj["paper_id"]
    for key in json_obj.keys():
        if (_recursion(json_obj[key])):
            print(paper_id)


def get_docs_with_abstract(subset):

    data_dir = os.path.join(os.getcwd(), base_dir+subset)
    print(len(os.listdir(data_dir)))

    i = 0
    for doc in tqdm(os.listdir(data_dir)):
        path2file = os.path.join(data_dir, doc)
        with open(path2file) as f:
            data = f.read()
            rawtext, paper_id = get_text(data)
            if rawtext:
                i +=1
                with open(os.path.join(os.getcwd(), base_dir+"/haveAbstract/"+paper_id+".txt"), "w", encoding="utf-8") as f:
                    f.write(rawtext)

    print(i)


def create_batches(batchsize=5000):
    """
    Merges single JSON files into bigger batch files, where the file is the key for the batch file.
    :param batchsize: number of files contained in on batch file
    """
    data_dir = os.path.join(os.getcwd(), base_dir+"haveAbstract")

    idx_batch ={}
    idx_doc ={}
    i = 0
    j = 0
    maxlen = len(os.listdir(data_dir))
    batch = 1
    for doc in tqdm(os.listdir(data_dir)):
        i += 1
        j += 1
        if j == maxlen:
            path2file = os.path.join(data_dir, doc)
            paper_id = doc[:-4]
            with open(path2file) as f:
                txt = f.read()
            idx_doc[paper_id] = txt
            idx_batch[batch] = idx_doc
        if i <= batchsize:
            path2file = os.path.join(data_dir, doc)
            paper_id = doc[:-4]
            with open(path2file) as f:
                txt = f.read()
            idx_doc[paper_id] = txt
        else:
            idx_batch[batch] = idx_doc
            idx_doc = {}
            batch += 1
            i = 1
            path2file = os.path.join(data_dir, doc)
            paper_id = doc[:-4]
            with open(path2file) as f:
                txt = f.read()
            idx_doc[paper_id] = txt
            idx_batch[batch] = idx_doc

    for idx in idx_batch.keys():
        with open("../data/v7/clustered/"+str(idx)+".json", "w", encoding="utf-8") as fout:

            fout.write(json.dumps(idx_batch[idx]))


subset = 'pdf_json'
get_docs_with_abstract(subset)

# merge the JSON files into bigger files with each one containing 5000 files
batchsize=5000
create_batches(batchsize)