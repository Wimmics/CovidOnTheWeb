import argparse
import copy
import collections
import json
import numpy as np
import os
import time
import torch

from collections import OrderedDict
from tqdm import tqdm
from torch import nn
from torch.utils.data import DataLoader, SequentialSampler
from transformers import BertForSequenceClassification, BertTokenizer
from pytorch_pretrained_bert.modeling import BertConfig, BertForMultipleChoice

from preprocessing_utils import get_text, tokenize_sentences
from data_processors import *
from models import BertForSequenceTaggingECAI, BertForSequenceTagging, BertForSequenceTaggingACTA




def preprocess_seq_input(data, tokenizer):
    sentences = data

    max_seq_length = -1

    feature_list =[]
    token_list = []

    for sentence in sentences:

        tokens_a = tokenizer.tokenize(sentence)

        if len(tokens_a) + 2 > max_seq_length:
            max_seq_length = len(tokens_a) + 2

        tokens = ["[CLS]"] + tokens_a + ["[SEP]"]
        token_list.append(tokens)
        segment_ids = [0] * len(tokens)
        input_ids = tokenizer.convert_tokens_to_ids(tokens)
        input_mask = [1] * len(input_ids)

        feature_list.append(
                InputFeatures(input_ids=input_ids,
                              input_mask=input_mask,
                              segment_ids=segment_ids,
                              label_ids=[0*len(input_ids)]))

    for f in feature_list:
        padding = [0] * (max_seq_length - len(f.input_ids))
        f.input_ids += padding
        f.input_mask += padding
        f.segment_ids += padding

        assert len(f.input_ids) == max_seq_length
        assert len(f.input_mask) == max_seq_length
        assert len(f.segment_ids) == max_seq_length

    all_input_ids = torch.tensor([f.input_ids for f in feature_list], dtype=torch.long)
    all_input_mask = torch.tensor([f.input_mask for f in feature_list], dtype=torch.long)
    all_segment_ids = torch.tensor([f.segment_ids for f in feature_list], dtype=torch.long)
    dataset = TensorDataset(all_input_ids, all_input_mask, all_segment_ids)

    return dataset, token_list

def extract_candidates(predictions, tokenized_sentences, label_map):
    def _clean_label_seq(label_seq, sentence):

        for j, token in enumerate(sentence):
            label = label_seq[j]

            if label == 'X':
                if "##" in token:
                    new_label = label_seq[j - 1]
                    if 'B-' in new_label:
                        label_seq[j] = new_label.replace('B-', 'I-')
                    else:
                        label_seq[j] = new_label

        # fixes [B-, 0, I-] to [B-, I-, I-]
        last = ""
        for i, label in enumerate(label_seq):
            if 'B-' in last:
                if label_seq[i] == 'O':
                    if i < len(label_seq)-1:
                        if 'I-' in label_seq[i+1]:
                            label_seq[i] = label_seq[i+1]
            last = label_seq[i]

        return label_seq

    candidates = []

    for i, sentence in enumerate(tokenized_sentences):
        pred_labels = []
        for idx in predictions[i]:
            pred_labels.append([key for key in label_map.keys() if label_map[key] == idx][0])

        pred_labels = _clean_label_seq(pred_labels, sentence)

        isCandidate = False
        candidate = []
        for j, token in enumerate(sentence):

            if 'B-' in pred_labels[j]:
                isCandidate = True
                candidate.append(token)
            elif 'I-' in pred_labels[j] and isCandidate:
                candidate.append(token)
            elif isCandidate and 'I-' not in pred_labels[j]:
                if len(candidate) > 5:
                    candidates.append((pred_labels[j-1], candidate))
                isCandidate = False
                candidate = []

    return candidates

def extract_pico(predictions, tokenized_sentences, label_map):

    candidates = []

    for i, sentence in enumerate(tokenized_sentences):
        candidate = []
        for j, tok in enumerate(sentence):
            if predictions[i][j] == 0:
                if candidate is not [] and predictions[i][j - 1] != '':
                    candidates.append((predictions[i][j - 1], candidate))
                candidate = []
                continue
            else:
                if predictions[i][j] == predictions[i][j-1]:
                    candidate.append(tok)
                else:
                    if candidate is not []:
                        candidates.append((predictions[i][j-1], candidate))
                        candidate = [tok]

    candidates = [(label_map[int(l)],t) for l,t in candidates if int(l) >1]
    return candidates

def _create_label_map(labels):
    label_map = collections.OrderedDict()
    inverse_map = {}
    for i, label in enumerate(labels):
        label_map[label] = i
        inverse_map[i] = label

    return label_map, inverse_map

def preprocess_linkprediction_input(data, tokenizer):

    idx_list = []
    dataset_list = []
    feature_list = []
    max_seq_length = -1
    for i, sent_a in enumerate(data):
        objs = []
        for j, sent_b in enumerate(data):
            if i == j:
                continue
            else:
                tokens = ["[CLS]"] + sent_a + ["[SEP]"]
                segment_ids = [0] * len(tokens)

                tokens += sent_b + ["[SEP]"]
                segment_ids += [1] * (len(sent_b) + 1)

                input_ids = tokenizer.convert_tokens_to_ids(tokens)
                input_mask = [1] * len(input_ids)
                feature_list.append(
                    InputFeatures(input_ids=input_ids,
                                  input_mask=input_mask,
                                  segment_ids=segment_ids,
                                  label_ids=1)
                )

                if len(tokens) > max_seq_length:
                    max_seq_length = len(tokens)
                objs.append(j)
        idx_list.append(objs)

        for f in feature_list:

            padding = [0] * (max_seq_length - len(f.input_ids))
            f.input_ids += padding
            f.input_mask += padding
            f.segment_ids += padding

            assert len(f.input_ids) == max_seq_length
            assert len(f.input_mask) == max_seq_length
            assert len(f.segment_ids) == max_seq_length

        all_input_ids = torch.tensor([f.input_ids for f in feature_list], dtype=torch.long)
        all_input_mask = torch.tensor([f.input_mask for f in feature_list], dtype=torch.long)
        all_segment_ids = torch.tensor([f.segment_ids for f in feature_list], dtype=torch.long)
        dataset = TensorDataset(all_input_ids, all_input_mask, all_segment_ids)
        dataset_list.append(dataset)

        feature_list = []
        max_seq_length = -1

    return dataset_list, idx_list

def preprocess_multichoice_input(data, tokenizer):

    def _select_field(features, field):
        return [
            [
                choice[field]
                for choice in feature.choices_features
            ]
            for feature in features
        ]

    longest = -1
    secondlongest = -1
    for c in data:
        if len(c[1]) >= longest:
            secondlongest = longest
            longest = len(c[1])
        elif len(c[1]) >= secondlongest:
            secondlongest = len(c[1])
    max_seq_length = longest + secondlongest + 3

    data = [c[1] for c in data]

    comp_mapping = OrderedDict([(i, c) for i,c in enumerate(data)])

    dataset_list = []
    features = []
    idx_list = []
    for subj_idx in comp_mapping.keys():

        choice_feature = []
        tmp_idx = []
        for obj_idx in comp_mapping.keys():
            if subj_idx == obj_idx:
                continue
            else:
                context_token = comp_mapping[subj_idx]
                ending_token = comp_mapping[obj_idx]
                tokens = ["[CLS]"] + context_token + ["[SEP]"] + ending_token + ["[SEP]"]
                segment_ids = [0] * (len(context_token) + 2) + [1] * (len(ending_token) + 1)
                input_ids = tokenizer.convert_tokens_to_ids(tokens)
                input_mask = [1] * len(input_ids)

                # Zero-pad up to the sequence length.
                padding = [0] * (max_seq_length - len(input_ids))
                input_ids += padding
                input_mask += padding
                segment_ids += padding

                assert len(input_ids) == max_seq_length
                assert len(input_mask) == max_seq_length
                assert len(segment_ids) == max_seq_length

                choice_feature.append((tokens, input_ids, input_mask, segment_ids))
                tmp_idx.append((subj_idx, obj_idx))

        idx_list.append(tmp_idx)
        features.append(
            MultiChoiceInputFeatures(
                example_id=subj_idx,
                choices_features=choice_feature,
                label=0
            )
        )

        all_input_ids = torch.tensor(_select_field(features, 'input_ids'), dtype=torch.long)
        all_input_mask = torch.tensor(_select_field(features, 'input_mask'), dtype=torch.long)
        all_segment_ids = torch.tensor(_select_field(features, 'segment_ids'), dtype=torch.long)
        dataset = TensorDataset(all_input_ids, all_input_mask, all_segment_ids)
        dataset_list.append(dataset)
        features = []

    return dataset_list, idx_list



class ActaProcessor():
    def __init__(self):
        self.sqmodel, self.sqtokenizer, self.sqprocessor = self.load_sq_model_ecai(do_lower_case=False)
        self.picomodel, self.picotokenizer, self.picoprocessor = self.load_pico_model(do_lower_case=False)
        self.mcmodel, self.mctokenizer = self.load_mc_model(do_lower_case=True)
        self.rcmodel, self.rctokenizer = self.load_rc_model(do_lower_case=True)

    def load_mc_model(self, model_dir='models/lp/', do_lower_case=True):
        num_choices = 5
        config_file = os.path.join(model_dir, 'bert_mc_config.json')
        model_file = os.path.join(model_dir, 'bert_mc_model.bin')
        config = BertConfig(config_file)
        model = BertForMultipleChoice(config, num_choices=num_choices)
        model.load_state_dict(
            torch.load(model_file, map_location=torch.device("cuda" if torch.cuda.is_available() else "cpu")))

        tokenizer = BertTokenizer.from_pretrained(model_dir, do_lower_case=do_lower_case)

        return model, tokenizer

    def load_sq_model_ecai(self, model_path='models/sq/ecai/', do_lower_case=True):
        model_path = os.path.join(os.getcwd(), model_path)

        model = BertForSequenceTaggingECAI.from_pretrained(model_path)
        model.eval()
        tokenizer = BertTokenizer.from_pretrained(model_path, do_lower_case=do_lower_case)

        processor = ArgMinSeqTagProcessor()

        return model, tokenizer, processor

    def load_pico_model(self, model_dir='models/sq/pico/', do_lower_case=True):

        config_file = os.path.join(model_dir, 'config.json')
        model_file = os.path.join(model_dir, 'pytorch_model.bin')

        config = BertConfig(config_file)
        model = BertForSequenceTaggingACTA(config, num_labels=5)
        model.load_state_dict(
            torch.load(model_file, map_location=torch.device("cuda" if torch.cuda.is_available() else "cpu")))

        tokenizer = BertTokenizer.from_pretrained(model_dir, do_lower_case=do_lower_case)

        processor = ArgMinSeqTagProcessor()

        return model, tokenizer, processor

    def load_rc_model(self, model_path='models/rc/', do_lower_case=True):
        model_path = os.path.join(os.getcwd(), model_path)
        model = BertForSequenceClassification.from_pretrained(model_path)
        tokenizer = BertTokenizer.from_pretrained(model_path, do_lower_case=do_lower_case)
        return model, tokenizer

    def link_prediction(self, candidates):

        candidate_copy = copy.deepcopy(candidates)

        if len(candidate_copy) <= 1:
            return []

        num_choices = len(candidate_copy) - 1

        if num_choices == 1:
            candidate_copy.append(candidate_copy[-1])

        links = []
        lp_dataset_list, idx_list = preprocess_multichoice_input(candidate_copy, self.mctokenizer)

        subj_idx = -1
        for lp_dataset in lp_dataset_list:
            subj_idx += 1
            self.mcmodel.num_choices = num_choices
            eval_sampler = SequentialSampler(lp_dataset)
            eval_dataloader = DataLoader(lp_dataset, sampler=eval_sampler)
            self.mcmodel.eval()
            y_preds = []
            token_ids = []
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

            for input_ids, input_mask, segment_ids in eval_dataloader:
                token_ids.append(input_ids)
                input_ids = input_ids.to(device)
                input_mask = input_mask.to(device)
                segment_ids = segment_ids.to(device)
                with torch.no_grad():
                    logits = self.mcmodel(input_ids, segment_ids, input_mask)
                logits = logits.detach().cpu()
                threshold = 0.5
                link_probabilities = nn.functional.softmax(logits, dim=1).numpy()[0]

                for i, link_prob in enumerate(link_probabilities):
                    if link_prob >= threshold:
                        y_preds.append((link_prob, idx_list[subj_idx][i]))

            for link in y_preds:
                prob, (subj, obj) = link
                if {"from": subj,
                    "to": obj,
                    "type": "support",
                    } not in links:
                    links.append({"from": subj,
                                  "to": obj,
                                  "type": "support",
                                  })

        return links

    def component_detection(self, sentences):
        labels = ["X", "B-Claim", "I-Claim", "B-Premise", "I-Premise", 'O']
        label_map, _ = _create_label_map(labels)
        predictions, inputs = self.predict(sentences, self.sqmodel, self.sqtokenizer, self.sqprocessor)
        tokenized_sentence = [self.sqtokenizer.convert_ids_to_tokens(np.array(sentence)) for sentence in inputs]
        candidates = extract_candidates(predictions, tokenized_sentence, label_map)
        c_idx = {}
        c_list = []
        for i, c in enumerate(candidates):
            c_idx[i] = c[0], ' '.join(c[1]).replace(' ##', '')
            if 'Claim' in c[0]:
                label = 'claim'
            else:
                label = 'evidence'

            c_list.append({
                "id": i,
                "text": ' '.join(c[1]).replace(' ##', ''),
                "type": label
            })

        return candidates, c_idx, c_list

    def pico_detection(self, sentences):
        labels = ["X", 'O', "Participants", "Intervention", "Outcome"]
        label_map, _ = _create_label_map(labels)
        label_map = {label_map[k]: k for k in label_map}

        tmp = []
        for s in sentences:
            if len(s.split()) > 64:
                x = s.split()
                tmp.append(' '.join(x[:int(len(x) / 2)]))
                tmp.append(' '.join(x[int(len(x) / 2):]))
            else:
                tmp.append(s)
        sentences = tmp
        dataset, seq_tokens = preprocess_seq_input(sentences, self.picotokenizer)

        predictions, inputs = self.predict(dataset, self.picomodel, self.picotokenizer, self.picoprocessor)
        tokenized_sentence = [self.picotokenizer.convert_ids_to_tokens(np.array(sentence)) for sentence in inputs]
        candidates = extract_pico(predictions, tokenized_sentence, label_map)

        picos = {}
        for i, c in enumerate(candidates):
            p = ' '.join(c[1]).replace(' ##', '')
            p = p.replace('##', '')
            picos[p] = c[0]
        return picos

    def relation_classification(self, data):
        rel_labels = ["noRel", "support", "attack"]
        rel_label_map, inverse_map = _create_label_map(rel_labels)

        if data["relations"] == []:
            return data

        rel_input = {}
        for rel in data["relations"]:
            subj_idx = rel["from"]
            obj_idx = rel["to"]

            for c in data["components"]:
                if c["id"] == subj_idx:
                    subj = c["text"]
                elif c["id"] == obj_idx:
                    obj = c["text"]
            rel_input[(subj_idx, obj_idx)] = (subj, obj)

        idx_list = {}
        feature_list = []
        max_seq_length = -1
        for i, (s_idx, o_idx) in enumerate(rel_input.keys()):
            idx_list[i] = {
                "from": s_idx,
                "to": o_idx}
            sent_a, sent_b = rel_input[s_idx, o_idx]

            sent_a = self.rctokenizer.tokenize(sent_a)
            sent_b = self.rctokenizer.tokenize(sent_b)

            tokens = ["[CLS]"] + sent_a + ["[SEP]"]
            segment_ids = [0] * len(tokens)

            tokens += sent_b + ["[SEP]"]
            segment_ids += [1] * (len(sent_b) + 1)

            input_ids = self.rctokenizer.convert_tokens_to_ids(tokens)
            input_mask = [1] * len(input_ids)
            feature_list.append(
                InputFeatures(input_ids=input_ids,
                              input_mask=input_mask,
                              segment_ids=segment_ids,
                              label_ids=1)
            )

            if len(tokens) > max_seq_length:
                max_seq_length = len(tokens)
        for f in feature_list:
            padding = [0] * (max_seq_length - len(f.input_ids))
            f.input_ids += padding
            f.input_mask += padding
            f.segment_ids += padding

            assert len(f.input_ids) == max_seq_length
            assert len(f.input_mask) == max_seq_length
            assert len(f.segment_ids) == max_seq_length

        all_input_ids = torch.tensor([f.input_ids for f in feature_list], dtype=torch.long)
        all_input_mask = torch.tensor([f.input_mask for f in feature_list], dtype=torch.long)
        all_segment_ids = torch.tensor([f.segment_ids for f in feature_list], dtype=torch.long)
        dataset = TensorDataset(all_input_ids, all_input_mask, all_segment_ids)

        threshold = 0.3
        outputs, input_ids = self.predict(dataset, self.rcmodel, self.rctokenizer)
        logits = outputs[0]
        link_probabilities = nn.functional.softmax(logits, dim=1).numpy()
        for j, probs in enumerate(link_probabilities):
            highest = np.argmax(probs)

            if highest > 0 and probs[highest] >= threshold:  # 0 is __noRel__
                idx_list[j]["type"] = inverse_map[highest]
            else:
                idx_list[j]["type"] = inverse_map[1]

        return data

    def predict(self, sentences, model, tokenizer, processor=None, max_seq_length=80):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        if isinstance(model, BertForSequenceClassification):
            dataset = sentences
        elif isinstance(model, BertForSequenceTaggingECAI):

            sentences = [(sent, "X") for sent in sentences]

            examples = processor._create_examples(sentences, "custom")
            features = processor.convert_examples_to_features(examples, max_seq_length=max_seq_length,
                                                              tokenizer=tokenizer, min_seq_length=5)
            if len(features) < 1:  # if all sentences are too short
                return None
            dataset = processor.features_to_dataset(features)

        elif isinstance(model, BertForSequenceTaggingACTA):
            dataset = sentences
        eval_sampler = SequentialSampler(dataset)
        dl = DataLoader(dataset, sampler=eval_sampler, batch_size=len(sentences))

        model.eval()
        for batch in dl:
            batch = tuple(t.to(device) for t in batch)
            with torch.no_grad():
                inputs = {"input_ids": batch[0], "attention_mask": batch[1]}

                outputs = model(**inputs)
                return outputs, inputs["input_ids"]

    def process_document(self, rawtext, paper_id, out_dir="./output"):

        if paper_id+ ".json" in os.listdir(out_dir):
            return

        sentences = tokenize_sentences(rawtext)

        # component detection
        candidates, c_idx, c_list = self.component_detection(sentences)
        components = [c_list[i]["text"] for i, c in enumerate(c_list)]

        if components == []:
            json_dict = {
                "paper_id": paper_id,
                "components": [],
                "relations": []
            }
            with open(os.path.join(out_dir, paper_id+ ".json"), 'w', encoding="UTF-8") as fw:
                fw.write(json.dumps(json_dict))
            return

        # pico detection
        picos = self.pico_detection(components)
        for i, c in enumerate(c_list):
            for pico in picos.keys():
                if len(pico) > 3:
                    if pico in c_list[i]["text"]:
                        p = picos[pico].lower()
                        if p in c_list[i].keys():
                            c_list[i][p].append({"text": pico})
                        else:
                            c_list[i][p] = [{"text": pico}]

        # link prediction
        links = self.link_prediction(candidates)

        json_dict = {
            "paper_id": paper_id,
            "components": c_list,
            "relations": links
        }

        # relation classification
        json_dict = self.relation_classification(json_dict)

        with open(os.path.join(out_dir, paper_id+ ".json"), 'w', encoding="UTF-8") as fw:
            fw.write(json.dumps(json_dict))


parser = argparse.ArgumentParser()
parser.add_argument("--fname",
                    required=True,
                    type=str)
parser.add_argument("--data_dir",
                    required=True,
                    type=str)
args = parser.parse_args()

start = time.time()
ap = ActaProcessor()
mid = time.time()
print("LOADING MODELS:", round(mid - start, 1))

with open(args.data_dir + args.fname + '.json') as fin:
    data = json.load(fin)

for doc in tqdm(data.keys()):
    mid = time.time()

    doc = "fe3697f73a430e718cb568b3dc441f207229bab8"
    raw = data[doc]


    ap.process_document(raw, doc)

    end = time.time()
    print("Processed %s:" % (doc), round(end - mid, 1))
    break

final = time.time()
print("RUN FOR ", round(final - start, 1))

