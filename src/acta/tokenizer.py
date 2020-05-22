from transformers import BertTokenizer
import os

class ExtendedBertTokenizer(BertTokenizer):
    """BertTokenizer which extends a token-based list of labels to WordPiece sub-token-based list.
    Params, Inputs, Outputs:
        See base class.
    """
    def __init__(self, *inputs, **kwargs):
        super().__init__(*inputs, **kwargs)

    def tokenize_with_label_extension(self, text, labels, copy_previous_label=False, extension_label='X'):
        '''
        Tokenize text and extends the label list to match the length of the tokenizer output.
        :param text: string
        :param labels: list of class labels
        :param copy_previous_label: boolean if previous label gets copied as new sub-token or if extension_label is used
        :param extension_label: if copy_previous_label is true, the new sub-token label will be this string
        :return: tokenized text and list of labels with matching length
        '''

        tok_text = self.tokenize(text)

        for i in range(0, len(tok_text)):
            if '##' in tok_text[i]:
                if copy_previous_label:
                    labels.insert(i, labels[i-1])
                else:
                    labels.insert(i, extension_label)

        return tok_text, labels

    def batch_to_conll(self, input_ids, label_ids, gold_label=None, processor=None, output_file=None):
        """

        :param input_ids: Tensor
        :param label_ids: ndarray
        :param gold_label: ndarray
        :param processor: Processor
        :return:
        """

        assert input_ids.shape == label_ids.shape

        sentences = []

        for i, _ in enumerate(input_ids):  # iterate over batch

            sentence = []
            y_pred = []

            for j, token_id in enumerate(input_ids[i].numpy()):  # iterate over tokens of one sequence

                token = self._convert_id_to_token(token_id)

                if processor is not None:
                    y_pred.append(processor.convert_ids_to_labels([int(label_ids[i][j])])[0])
                else:
                    y_pred.append(label_ids[i][j])

                sentence.append(token)

            if gold_label is not None:
                if processor is not None:
                    y_true = processor.convert_ids_to_labels(list(gold_label[i]))
                else:
                    y_true = gold_label[i]  # ndarray
                sentences.append((sentence, y_pred, y_true))
            else:
                sentences.append((sentence, y_pred))

        #with open(output_file, "a") as writer:
        with open(output_file, "a") as writer:
            for sentence, preds, labels in sentences:
                for i, w in enumerate(sentence):
                    if w in {"[CLS]", "[SEP]", "[PAD]"}:
                        continue
                    writer.write("%s\t%s\t%s\n" % (w, preds[i], labels[i]))
                writer.write("\n")
