import torch
from torch import nn
from transformers.modeling_bert import BertModel

from pytorch_pretrained_bert.modeling import BertEmbeddings, BertEncoder
from torchcrf import CRF


from pytorch_pretrained_bert.modeling import BertPreTrainedModel
class BertForSequenceTaggingACTA(BertPreTrainedModel):

    def __init__(self, config, num_labels):
        super(BertForSequenceTaggingACTA, self).__init__(config)
        self.num_labels = num_labels
        self.embeddings = BertEmbeddings(config)
        self.encoder = BertEncoder(config)
        self.gru = nn.GRU(config.hidden_size, config.hidden_size, batch_first=True, bidirectional=True)

        self.crf = CRF(num_labels, batch_first=True)

        self.clf = nn.Linear(2*config.hidden_size, num_labels)

        #nn.init.xavier_uniform_(self.clf.weight)
        #self.clf.bias.data.fill_(0.01)
        #self.pooler = BertPooler(config)
        self.apply(self.init_bert_weights)

    def forward(self, input_ids, token_type_ids=None, attention_mask=None, labels=None):
        if attention_mask is None:
            attention_mask = torch.ones_like(input_ids)
        if token_type_ids is None:
            token_type_ids = torch.zeros_like(input_ids)

        # We create a 3D attention mask from a 2D tensor mask.
        # Sizes are [batch_size, 1, 1, to_seq_length]
        # So we can broadcast to [batch_size, num_heads, from_seq_length, to_seq_length]
        # this attention mask is more simple than the triangular masking of causal attention
        # used in OpenAI GPT, we just need to prepare the broadcast dimension here.
        extended_attention_mask = attention_mask.unsqueeze(1).unsqueeze(2)

        # Since attention_mask is 1.0 for positions we want to attend and 0.0 for
        # masked positions, this operation will create a tensor which is 0.0 for
        # positions we want to attend and -10000.0 for masked positions.
        # Since we are adding it to the raw scores before the softmax, this is
        # effectively the same as removing these entirely.
        extended_attention_mask = extended_attention_mask.to(dtype=next(self.parameters()).dtype)  # fp16 compatibility
        extended_attention_mask = (1.0 - extended_attention_mask) * -10000.0

        embedding_output = self.embeddings(input_ids, token_type_ids)
        encoded_layers = self.encoder(embedding_output,
                                      extended_attention_mask,
                                      output_all_encoded_layers=False)
        sequence_output = encoded_layers[-1]

        gru_out, _ = self.gru(sequence_output)


        #pooled_output = self.pooler(sequence_output)
        emissions = self.clf(gru_out)

        if labels is not None:
            #output = logits.view(-1, self.num_labels)
            #target = labels.view(-1)
            #loss_fct = nn.CrossEntropyLoss()
            #loss = loss_fct(output, target)
            loss = self.crf(emissions, labels)
            return -1*loss
        else:
            path = self.crf.decode(emissions)
            path = torch.LongTensor(path)
            return path

from transformers.modeling_bert import BertModel, BertPreTrainedModel
class BertForSequenceTagging(BertPreTrainedModel):

    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels

        self.bert = BertModel(config)

        #self.rnn = nn.GRU(config.hidden_size, config.hidden_size, batch_first=True, bidirectional=True)
        self.rnn = nn.LSTM(config.hidden_size, config.hidden_size, batch_first=True, bidirectional=True)

        self.crf = CRF(config.num_labels, batch_first=True)
        self.classifier = nn.Linear(2 * config.hidden_size, config.num_labels)

        self.init_weights()

    def forward(
        self,
        input_ids=None,
        attention_mask=None,
        token_type_ids=None,
        position_ids=None,
        head_mask=None,
        inputs_embeds=None,
        labels=None,
    ):

        outputs = self.bert(
            input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            head_mask=head_mask,
            inputs_embeds=inputs_embeds,
        )

        sequence_output = outputs[0]

        rnn_out, _ = self.rnn(sequence_output)
        emissions = self.classifier(rnn_out)

        if labels is not None:
            loss = self.crf(emissions, labels)

            path = self.crf.decode(emissions)
            path = torch.LongTensor(path)

            return (-1*loss, emissions, path)
        else:
            path = self.crf.decode(emissions)
            path = torch.LongTensor(path)

            return path

class BertForSequenceTaggingECAI(BertPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels

        self.bert = BertModel(config)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)

        self.rnn = nn.GRU(config.hidden_size, config.hidden_size, batch_first=True, bidirectional=True)
        # self.rnn = nn.LSTM(config.hidden_size, config.hidden_size, batch_first=True, bidirectional=True)

        self.crf = CRF(config.num_labels, batch_first=True)
        self.classifier = nn.Linear(2 * config.hidden_size, config.num_labels)

        self.init_weights()

    def forward(
            self,
            input_ids=None,
            attention_mask=None,
            token_type_ids=None,
            position_ids=None,
            head_mask=None,
            inputs_embeds=None,
            labels=None,
    ):

        # print("INPUT")
        # print(type(labels))
        # print(labels)
        # print(labels.size())

        outputs = self.bert(
            input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            head_mask=head_mask,
            inputs_embeds=inputs_embeds,
        )

        # pooled_output = outputs[1]
        # pooled_output = self.dropout(pooled_output)
        # hidden_states = outputs[2]

        sequence_output = outputs[0]
        sequence_output = self.dropout(sequence_output)

        rnn_out, _ = self.rnn(sequence_output)
        emissions = self.classifier(rnn_out)

        if labels is not None:
            # output = logits.view(-1, self.num_labels)
            # target = labels.view(-1)
            # loss_fct = nn.CrossEntropyLoss()
            # loss = loss_fct(output, target)
            loss = self.crf(emissions, labels)

            path = self.crf.decode(emissions)
            path = torch.LongTensor(path)

            return (-1 * loss, emissions, path)
        else:
            path = self.crf.decode(emissions)
            path = torch.LongTensor(path)

            return path