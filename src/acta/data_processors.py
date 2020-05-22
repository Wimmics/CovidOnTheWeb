import csv
import sys
import os
import collections
import torch
from torch.utils.data import TensorDataset
from transformers import BasicTokenizer

class MultiChoiceExample(object):
    """A single training/test example for the SWAG dataset."""
    def __init__(self,
                 swag_id,
                 context_sentence,
                 ending_0,
                 ending_1,
                 ending_2,
                 ending_3,
                 ending_4,
                 ending_5,
                 label = None):
        self.swag_id = swag_id
        self.context_sentence = context_sentence
        self.endings = [
            ending_0,
            ending_1,
            ending_2,
            ending_3,
            ending_4,
            ending_5,
        ]
        self.label = label

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        l = [
            "swag_id: {}".format(self.swag_id),
            "context_sentence: {}".format(self.context_sentence),
            "ending_0: {}".format(self.endings[0]),
            "ending_1: {}".format(self.endings[1]),
            "ending_2: {}".format(self.endings[2]),
            "ending_3: {}".format(self.endings[3]),
            "ending_4: {}".format(self.endings[4]),
            "ending_5: {}".format(self.endings[5]),
        ]

        if self.label is not None:
            l.append("label: {}".format(self.label))

        return ", ".join(l)

    @classmethod
    def truncate_seq_pair(cls, tokens_a, tokens_b, max_length):
        """Truncates a sequence pair in place to the maximum length."""

        # This is a simple heuristic which will always truncate the longer sequence
        # one token at a time. This makes more sense than truncating an equal percent
        # of tokens from each, since if one sequence is very short then each token
        # that's truncated likely contains more information than a longer sequence.
        while True:
            total_length = len(tokens_a) + len(tokens_b)
            if total_length <= max_length:
                break
            if len(tokens_a) > len(tokens_b):
                tokens_a.pop()
            else:
                tokens_b.pop()


class MultiChoiceInputFeatures(object):
    def __init__(self,
                 example_id,
                 choices_features,
                 label

    ):
        self.example_id = example_id
        self.choices_features = [
            {
                'input_ids': input_ids,
                'input_mask': input_mask,
                'segment_ids': segment_ids
            }
            for _, input_ids, input_mask, segment_ids in choices_features
        ]
        self.label = label

    @classmethod
    def select_field(cls, features, field):
        return [
            [
                choice[field]
                for choice in feature.choices_features
            ]
            for feature in features
        ]

class InputExample(object):
    """A single training/test example for simple sequence classification."""

    def __init__(self, guid, text_a, text_b=None, labels=None):
        """Constructs a InputExample.
        Args:
            guid: Unique id for the example.
            text_a: string. The untokenized text of the first sequence. For single
            sequence tasks, only this sequence must be specified.
            text_b: (Optional) string. The untokenized text of the second sequence.
            Only must be specified for sequence pair tasks.
            label: (Optional) string. The label of the example. This should be
            specified for train and dev examples, but not for test examples.
        """
        self.guid = guid
        self.text_a = text_a
        self.text_b = text_b
        self.labels = labels

    @classmethod
    def truncate_seq_pair(cls, tokens_a, tokens_b, max_length):
        """Truncates a sequence pair in place to the maximum length."""

        # This is a simple heuristic which will always truncate the longer sequence
        # one token at a time. This makes more sense than truncating an equal percent
        # of tokens from each, since if one sequence is very short then each token
        # that's truncated likely contains more information than a longer sequence.
        while True:
            total_length = len(tokens_a) + len(tokens_b)
            if total_length <= max_length:
                break
            if len(tokens_a) > len(tokens_b):
                tokens_a.pop()
            else:
                tokens_b.pop()


class InputFeatures(object):
    """A single set of features of data."""

    def __init__(self, input_ids, input_mask, segment_ids, label_ids):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.label_ids = label_ids


class DataProcessor(object):
    """Base class for data converters for sequence classification data sets."""

    def get_train_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the train set."""
        raise NotImplementedError()

    def get_dev_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the dev set."""
        raise NotImplementedError()

    def get_labels(self):
        """Gets the list of labels for this data set."""
        raise NotImplementedError()

    def convert_examples_to_features(self, examples, max_seq_length, tokenizer,
                                    logger=None,
                                    forSequenceTagging=False,
                                    min_seq_length=None,
                                    cls_token='[CLS]',
                                    sep_token_extra=False,
                                    sep_token = '[SEP]'):
        """Loads a data file into a list of `InputBatch`s."""

        features = []
        for (ex_index, example) in enumerate(examples):
            tokens_b = None
            if forSequenceTagging:
                tokens_a, labels = tokenizer.tokenize_with_label_extension(example.text_a, example.labels, copy_previous_label=True)

                # Account for [CLS] and [SEP] with "- 2"
                if len(tokens_a) > max_seq_length - 2:
                    tokens_a = tokens_a[:(max_seq_length - 2)]
                    labels = labels[:(max_seq_length - 2)]
                labels = ["X"] + labels + ["X"]
            else:

                tokens_a = tokenizer.tokenize(example.text_a)

                if example.text_b:
                    tokens_b = tokenizer.tokenize(example.text_b)
                    # Modifies `tokens_a` and `tokens_b` in place so that the total
                    # length is less than the specified length.
                    # Account for [CLS], [SEP], [SEP] with "- 3"
                    InputExample.truncate_seq_pair(tokens_a, tokens_b, max_seq_length - 3)
                else:
                    # Account for [CLS] and [SEP] with "- 2"
                    if len(tokens_a) > max_seq_length - 2:
                        tokens_a = tokens_a[:(max_seq_length - 2)]

            # The convention in BERT is:
            # (a) For sequence pairs:
            #  tokens:   [CLS] is this jack ##son ##ville ? [SEP] no it is not . [SEP]
            #  type_ids: 0   0  0    0    0     0       0 0    1  1  1  1   1 1
            # (b) For single sequences:
            #  tokens:   [CLS] the dog is hairy . [SEP]
            #  type_ids: 0   0   0   0  0     0 0
            #
            # Where "type_ids" are used to indicate whether this is the first
            # sequence or the second sequence. The embedding vectors for `type=0` and
            # `type=1` were learned during pre-training and are added to the wordpiece
            # embedding vector (and position vector). This is not *strictly* necessary
            # since the [SEP] token unambigiously separates the sequences, but it makes
            # it easier for the model to learn the concept of sequences.
            #
            # For classification tasks, the first vector (corresponding to [CLS]) is
            # used as as the "sentence vector". Note that this only makes sense because
            # the entire model is fine-tuned.
            tokens = [cls_token] + tokens_a + [sep_token]

            if sep_token_extra:
                # roberta uses an extra separator b/w pairs of sentences
                tokens += [sep_token]

            segment_ids = [0] * len(tokens)

            if tokens_b:
                tokens += tokens_b + [sep_token]
                segment_ids += [1] * (len(tokens_b) + 1)


            input_ids = tokenizer.convert_tokens_to_ids(tokens)

            if min_seq_length is not None:
                if len(input_ids) < min_seq_length:
                    continue

            # The mask has 1 for real tokens and 0 for padding tokens. Only real
            # tokens are attended to.
            input_mask = [1] * len(input_ids)

            # Zero-pad up to the sequence length.
            padding = [0] * (max_seq_length - len(input_ids))
            input_ids += padding
            input_mask += padding
            segment_ids += padding

            if forSequenceTagging:
                label_ids = self.convert_labels_to_ids(labels)
                label_ids += padding
                assert len(label_ids) == max_seq_length
            else:
                label_list = self.get_labels()
                label_map = {label: i for i, label in enumerate(label_list)}
                label_ids = label_map[example.labels]

            assert len(input_ids) == max_seq_length
            assert len(input_mask) == max_seq_length
            assert len(segment_ids) == max_seq_length

            if ex_index < 10 and logger is not None:
                logger.info("*** Example ***")
                logger.info("guid: %s" % (example.guid))
                logger.info("tokens: %s" % " ".join(
                    [str(x) for x in tokens]))
                logger.info("input_ids: %s" % " ".join([str(x) for x in input_ids]))
                logger.info("input_mask: %s" % " ".join([str(x) for x in input_mask]))
                logger.info(
                    "segment_ids: %s" % " ".join([str(x) for x in segment_ids]))
                if forSequenceTagging:
                    logger.info("label_ids: %s" % " ".join([str(x) for x in label_ids]))
                else:
                    logger.info("label_id: %s" % " ".join(str(label_ids)))

            features.append(
                InputFeatures(input_ids=input_ids,
                              input_mask=input_mask,
                              segment_ids=segment_ids,
                              label_ids=label_ids))
        return features

    @classmethod
    def features_to_dataset(cls, feature_list, isMultiChoice=None):

        if isMultiChoice:
            all_input_ids = torch.tensor(MultiChoiceInputFeatures.select_field(feature_list, 'input_ids'), dtype=torch.long)
            all_input_mask = torch.tensor(MultiChoiceInputFeatures.select_field(feature_list, 'input_mask'), dtype=torch.long)
            all_segment_ids = torch.tensor(MultiChoiceInputFeatures.select_field(feature_list, 'segment_ids'), dtype=torch.long)
            all_label = torch.tensor([f.label for f in feature_list], dtype=torch.long)
            dataset = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_label)
        else:
            all_input_ids = torch.tensor([f.input_ids for f in feature_list], dtype=torch.long)
            all_input_mask = torch.tensor([f.input_mask for f in feature_list], dtype=torch.long)
            all_segment_ids = torch.tensor([f.segment_ids for f in feature_list], dtype=torch.long)
            all_label_ids = torch.tensor([f.label_ids for f in feature_list], dtype=torch.long)
            dataset = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_label_ids)

        return dataset

    @classmethod
    def _read_tsv(cls, input_file, quotechar=None):
        """Reads a tab separated value file."""
        with open(input_file, "r") as f:
            reader = csv.reader(f, delimiter="\t", quotechar=quotechar)
            lines = []
            for line in reader:
                if sys.version_info[0] == 2:
                    line = list(unicode(cell, 'utf-8') for cell in line)
                lines.append(line)
            return lines

    @classmethod
    def _read_conll(cls, input_file, token_column=1, label_column=4, replace=None):
        """Reads a conll type file."""
        with open(input_file, "r", encoding='utf-8') as f:
            lines = f.readlines()
            lines.append("\n") #workaround adding a stop criteria for last sentence iteration

            sentences = []
            try:
                lines[0].split('\t')[label_column]
            except IndexError as err:
                print('Label column', err)
                raise

            tokenizer = BasicTokenizer()
            sent_tokens = []
            sent_labels = []

            for line in lines:

                line = line.split('\t')

                if len(line) < 2:
                    assert len(sent_tokens) == len(sent_labels)
                    if sent_tokens == []:
                        continue

                    if replace == None:
                        sentences.append([' '.join(sent_tokens), sent_labels])
                    else:
                        sent_labels = [replace[label] if label in replace.keys() else label for label in sent_labels]
                        sentences.append([' '.join(sent_tokens), sent_labels])
                    sent_tokens = []
                    sent_labels = []
                    continue

                token = line[token_column]
                label = line[label_column].replace('\n', '')
                tokenized = tokenizer.tokenize(token)

                if len(tokenized) > 1:

                    for i in range(len(tokenized)):
                        if 'B-' in label:
                            if i < 1:
                                sent_tokens.append(tokenized[i])
                                sent_labels.append(label)
                            else:
                                sent_tokens.append(tokenized[i])
                                #sent_labels.append(label.replace('B-', 'I-')) #if only the first token should be B-
                                sent_labels.append(label)
                        else:
                            sent_tokens.append(tokenized[i])
                            sent_labels.append(label)

                else:
                    sent_tokens.append(tokenized[0])
                    sent_labels.append(label)

        return sentences


class ArgMinSeqTagProcessor(DataProcessor):
    """Processor for RCT data set (CoNLL format)"""

    def __init__(self):
        self.labels = ["X", "B-Claim", "I-Claim", "B-Premise", "I-Premise", 'O']
        self.label_map = self._create_label_map()
        self.replace_labels = {
            'B-MajorClaim':'B-Claim',
            'I-MajorClaim': 'I-Claim',
        }


    def _create_label_map(self):
        label_map = collections.OrderedDict()
        for i, label in enumerate(self.labels):
            label_map[label] = i
        return label_map

    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_conll(os.path.join(data_dir, "train.conll"), replace=self.replace_labels), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_conll(os.path.join(data_dir, "dev.conll"), replace=self.replace_labels), "dev")

    def get_test_examples(self, data_dir, setname="test.conll"):
        """See base class."""
        return self._create_examples(
            self._read_conll(os.path.join(data_dir, setname), replace=self.replace_labels), "test")

    def get_labels(self):
        """ See base class."""
        return self.labels

    def convert_labels_to_ids(self, labels):
        idx_list = []
        for label in labels:
            idx_list.append(self.label_map[label])
        return idx_list

    def convert_ids_to_labels(self, idx_list):
        labels_list = []
        for idx in idx_list:
            labels_list.append([key for key in self.label_map.keys() if self.label_map[key] == idx][0])
        return labels_list

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            guid = "%s-%s" % (set_type, str(i))
            text_a = line[0]
            labels = line[-1]
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=None, labels=labels))
        return examples


class ArgMinRelClassProcessor(DataProcessor):
    """Processor for the RCT data set (for training)."""

    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train_relations.tsv")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev_relations.tsv")), "dev")

    def get_test_examples(self, data_dir, setname="test_relations.tsv"):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, setname)), "test")

    def get_labels(self):
        """See base class."""
        return ["__label__noRel", "__label__Support", "__label__Attack"]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            # skip first line (e.g. PE dataset)
            #if i == 0:
            #    continue
            guid = "%s-%s" % (set_type, line[0])
            text_a = line[1]
            text_b = line[2]
            label = line[0]
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=text_b, labels=label))
        return examples


class ArgMinRelClassForMultiChoiceProcessor(ArgMinRelClassProcessor):
    """Processor for the RCT data set (for the relation classification in the multiple choice training)."""

    def get_labels(self):
        """See base class."""
        return ["__label__Support", "__label__Attack"]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):


            if line[0] == "__label__noRel":
                continue

            guid = "%s-%s" % (set_type, line[0])
            text_a = line[1]
            text_b = line[2]
            label = line[0]
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=text_b, labels=label))
        return examples


class ArgMinMultiChoiceLinkProcessor(DataProcessor):

    def __init__(self):
        super().__init__()
        self.labelmap = {
            "NoRelation": 2,
            "Support": 0,
            "Attack": 1,
            "Partial-Attack": 1
        }


    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train_mc.tsv")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev_mc.tsv")), "dev")

    def get_test_examples(self, data_dir, setname="test_mc.tsv"):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, setname)), "test")

    def get_labels(self):
        """ See base class."""
        return ["0", "1", "2", "3", "4", "5"]

    def _create_examples(self, lines, set_type):
        examples = []

        for i, line in enumerate(lines):
            guid = "%s-%s" % (set_type, str(i))
            context_sentence = line[0]
            ending_0 = line[1]
            ending_1 = line[2]
            ending_2 = line[3]
            ending_3 = line[4]
            ending_4 = line[5]
            ending_5 = line[6]
            #label = int(line[7])
            label = (int(line[7]), self.labelmap[line[8]])
            examples.append(MultiChoiceExample(
                swag_id=guid,
                context_sentence=context_sentence,
                ending_0=ending_0,
                ending_1=ending_1,
                ending_2=ending_2,
                ending_3=ending_3,
                ending_4=ending_4,
                ending_5=ending_5,
                label=label
            ))
        return examples

    def convert_examples_to_features(self, examples, tokenizer, max_seq_length, logger=None):
        """Loads a data file into a list of `InputBatch`s."""

        # Swag is a multiple choice task. To perform this task using Bert,
        # we will use the formatting proposed in "Improving Language
        # Understanding by Generative Pre-Training" and suggested by
        # @jacobdevlin-google in this issue
        # https://github.com/google-research/bert/issues/38.
        #
        # Each choice will correspond to a sample on which we run the
        # inference. For a given Swag example, we will create the 4
        # following inputs:
        # - [CLS] context [SEP] choice_1 [SEP]
        # - [CLS] context [SEP] choice_2 [SEP]
        # - [CLS] context [SEP] choice_3 [SEP]
        # - [CLS] context [SEP] choice_4 [SEP]
        # The model will output a single value for each input. To get the
        # final decision of the model, we will run a softmax over these 4
        # outputs.
        features = []
        for example_index, example in enumerate(examples):
            context_tokens = tokenizer.tokenize(example.context_sentence)

            choices_features = []
            for ending_index, ending in enumerate(example.endings):
                # We create a copy of the context tokens in order to be
                # able to shrink it according to ending_tokens
                context_tokens_choice = context_tokens[:]
                ending_tokens = tokenizer.tokenize(ending)
                # Modifies `context_tokens_choice` and `ending_tokens` in
                # place so that the total length is less than the
                # specified length.  Account for [CLS], [SEP], [SEP] with
                # "- 3"
                MultiChoiceExample.truncate_seq_pair(context_tokens_choice, ending_tokens, max_seq_length - 3)

                tokens = ["[CLS]"] + context_tokens_choice + ["[SEP]"] + ending_tokens + ["[SEP]"]
                segment_ids = [0] * (len(context_tokens_choice) + 2) + [1] * (len(ending_tokens) + 1)

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

                choices_features.append((tokens, input_ids, input_mask, segment_ids))

            label = example.label
            if example_index < 3 and logger is not None:
                logger.info("*** Example ***")
                logger.info("example_id: {}".format(example.swag_id))
                for choice_idx, (tokens, input_ids, input_mask, segment_ids) in enumerate(choices_features):
                    logger.info("choice_idx: {}".format(choice_idx))
                    logger.info("tokens: {}".format(' '.join(tokens)))
                    logger.info("input_ids: {}".format(' '.join(map(str, input_ids))))
                    logger.info("input_mask: {}".format(' '.join(map(str, input_mask))))
                    logger.info("segment_ids: {}".format(' '.join(map(str, segment_ids))))
                    logger.info("label: {}".format(label))

            features.append(
                MultiChoiceInputFeatures(
                    example_id=example.swag_id,
                    choices_features=choices_features,
                    label=label
                )
            )

        return features


processors = {
    "seqtag": ArgMinSeqTagProcessor,
    "relclass": ArgMinRelClassProcessor,
    "multichoice": (ArgMinRelClassForMultiChoiceProcessor, ArgMinMultiChoiceLinkProcessor)
}

output_modes = {
    "seqtag": "sequencetagging",
    "relclass": "classification",
    "multichoice": "classification",
}