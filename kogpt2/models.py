from django.db import models

# Create your models here.
import torch
import transformers
from transformers import AutoModelWithLMHead, PreTrainedTokenizerFast
from fastai.text.all import *
import re
import fastai
import pandas as pd
import re
from icecream import ic


# from pykospacing import Spacing

class TransformersTokenizer(Transform):
    def __init__(self, tokenizer): self.tokenizer = tokenizer

    def encodes(self, x):
        toks = self.tokenizer.tokenize(x)
        return tensor(self.tokenizer.convert_tokens_to_ids(toks))

    def decodes(self, x): return TitledStr(self.tokenizer.decode(x.cpu().numpy()))


class DropOutput(Callback):
    def after_pred(self): self.learn.pred = self.pred[0]


class Solution:
    def __init__(self, text):
        self.text = text
        self.tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
                                                                 bos_token='</s>', eos_token='</s>', unk_token='<unk>',
                                                                 pad_token='<pad>', mask_token='<mask>')
        self.model = AutoModelWithLMHead.from_pretrained("skt/kogpt2-base-v2")

    #def hook(self):
        # self.version()
        # self.csv_to_txt()
        # data = self.preprocess()
        # dls = self.dataloader(data)
        # learn = self.fit(dls)
        # self.generate(learn)
        # self.save_model(learn)

    def version(self):
        print(torch.__version__)
        print(transformers.__version__)
        print(fastai.__version__)

    def test(self):
        text = """ 옛날 옛날 어느 마을에 흥부와 놀부 형제가 """
        model = self.model
        tokenizer = self.tokenizer
        input_ids = tokenizer.encode(text)
        gen_ids = model.generate(torch.tensor([input_ids]),
                                 max_length=128,
                                 repetition_penalty=2.0,
                                 pad_token_id=tokenizer.pad_token_id,
                                 eos_token_id=tokenizer.eos_token_id,
                                 bos_token_id=tokenizer.bos_token_id,
                                 use_cache=True
                                 )
        generated = tokenizer.decode(gen_ids[0, :].tolist())
        print(generated)

    def csv_to_txt(self):
        df = pd.read_csv('./data/book_report_data.csv', index_col=0)
        df.drop_duplicates(keep='first', inplace=True, ignore_index=False)
        df = df.to_csv('./data/book_report_data.txt', index=False)

    def preprocess(self):
        # spacing = Spacing()
        with open('data/book_report_data.txt', 'r', encoding='utf-8') as f:
            data = f.read()
        data = " ".join(data.split())
        data = data.replace('\n|\t', ' ')
        # data = data.replace(" ",'')
        # data = spacing(data)
        data = re.sub('[-=+,#/\:^$@*\"※~&%ㆍ』\\‘|\(\)\[\]\<\>`\'…》]', '', data)
        data = re.sub('[a-zA-Z]', '', data)
        # with open('data/book_report_preprocess.txt') as f:
        #     f.write(data)
        return data

    def dataloader(self, data):
        # split data
        train = data[:int(len(data) * 0.9)]
        test = data[int(len(data) * 0.9):]
        splits = [[0], [1]]

        # init dataloader
        tls = TfmdLists([train, test], TransformersTokenizer(self.tokenizer), splits=splits, dl_type=LMDataLoader)
        batch, seq_len = 4, 256
        dls = tls.dataloaders(bs=batch, seq_len=seq_len)
        return dls

    def fit(self, dls):
        model = self.model
        learn = Learner(dls, model, loss_func=CrossEntropyLossFlat(), cbs=[DropOutput], metrics=Perplexity()).to_fp16()
        lr = learn.lr_find()
        print(lr)
        learn.fit_one_cycle(1, lr)
        return learn

    def generate(self, learn):
        tokenizer = self.tokenizer
        prompt = '여행가고 싶어지는'
        prompt_ids = tokenizer.encode(prompt)
        inp = tensor(prompt_ids)[None].cuda()
        preds = learn.model.generate(inp,
                                     max_length=128,
                                     pad_token_id=tokenizer.pad_token_id,
                                     eos_token_id=tokenizer.eos_token_id,
                                     bos_token_id=tokenizer.bos_token_id,
                                     repetition_penalty=2.0,
                                     use_cache=True
                                     )
        result = tokenizer.decode(preds[0].cpu().numpy())
        print(result)

    def save_model(self, learn):
        learn.model.save_pretrained("./models/generate_model")

    def result(self):
        print('result 진입')
        tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
                                                                 bos_token='</s>', eos_token='</s>', unk_token='<unk>',
                                                                 pad_token='<pad>', mask_token='<mask>')
        model = AutoModelWithLMHead.from_pretrained("models/models/kogpt2_bookreport_backup50")
        input_ids = tokenizer.encode(self.text)
        gen_ids = model.generate(torch.tensor([input_ids]),
                                 max_length=128,
                                 repetition_penalty=2.0,
                                 pad_token_id=tokenizer.pad_token_id,
                                 eos_token_id=tokenizer.eos_token_id,
                                 bos_token_id=tokenizer.bos_token_id,
                                 use_cache=True
                                 )
        generated = tokenizer.decode(gen_ids[0, :].tolist())
        print(generated)
        return generated