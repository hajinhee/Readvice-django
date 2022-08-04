from django.db import models

# Create your models here.
import torch
from transformers import PreTrainedTokenizerFast
from torch.utils.data import Dataset
import gluonnlp as nlp
import numpy as np
import random
from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model

from torch import nn
import torch


class BERTClassifier(nn.Module):
    def __init__(self,
                 bert,
                 hidden_size=768,
                 num_classes=5,  ##클래스 수 조정##
                 dr_rate=None,
                 params=None):
        super(BERTClassifier, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate

        self.classifier = nn.Linear(hidden_size, num_classes)
        if dr_rate:
            self.dropout = nn.Dropout(p=dr_rate)

    def gen_attention_mask(self, token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
        return attention_mask.float()

    def forward(self, token_ids, valid_length, segment_ids):
        attention_mask = self.gen_attention_mask(token_ids, valid_length)

        _, pooler = self.bert(input_ids=token_ids, token_type_ids=segment_ids.long(),
                              attention_mask=attention_mask.float().to(token_ids.device))
        if self.dr_rate:
            out = self.dropout(pooler)
        return self.classifier(out)


class BERTDataset(Dataset):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, max_len,
                 pad, pair):
        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len, pad=pad, pair=pair)

        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]

    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i],))

    def __len__(self):
        return (len(self.labels))


class Chatbot():
    def __init__(self):
        self.Q_TKN = "<usr>"
        self.A_TKN = "<sys>"
        self.BOS = '</s>'
        self.EOS = '</s>'
        self.MASK = '<unused0>'
        self.SENT = '<unused1>'
        self.PAD = '<pad>'
        self.UNK = '<unk>'
        self.tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
                                                                 bos_token=self.BOS, eos_token=self.EOS,
                                                                 unk_token=self.UNK, pad_token=self.PAD,
                                                                 mask_token=self.MASK)


    # 모델 불러오기
    def execute_model(self):
        device = torch.device('cpu')
        PATH = 'C:/Users/jinhee/project_readvice/readvice/chatbot/save/chatbot_v80.pt'
        model = torch.load(PATH, map_location=device)

        model.eval()

        with torch.no_grad():
            while 1:
                q = input("user > ").strip()
                if q == "바이":
                    print("chatbot > 또 만나요^^")
                    break
                elif q == "책추천해줘":
                    Emotion.emotion(self)
                    continue
                elif q == "책 추천해줘":
                    Emotion.emotion(self)
                    continue
                elif q == "책 추천":
                    Emotion.emotion(self)
                    continue
                a = ""
                while 1:
                    input_ids = torch.LongTensor(
                        self.tokenizer.encode(self.Q_TKN + q + self.SENT + self.A_TKN + a)).unsqueeze(dim=0)
                    pred = model(input_ids)
                    pred = pred.logits
                    gen = self.tokenizer.convert_ids_to_tokens(torch.argmax(pred, dim=-1).squeeze().numpy().tolist())[
                        -1]
                    if gen == self.EOS:
                        break
                    a += gen.replace("▁", " ")
                print("chatbot > {}".format(a.strip()))


class Emotion:
    def __init__(self):
        self.max_len = 100
        self.batch_size = 16
        bertmodel, vocab = get_pytorch_kobert_model()
        # 토큰화
        tokenizer = get_tokenizer()
        self.tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)

    def emotion(self):
        max_len = 100
        batch_size = 16
        bertmodel, vocab = get_pytorch_kobert_model()
        # 토큰화
        tokenizer = get_tokenizer()
        tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)
        device = torch.device("cuda:0")

        with torch.no_grad():
            end = 1
            while end == 1:
                sentence = input("오늘 기분은 어떠세요?" + '\n')
                model = torch.load('C:/Users/jinhee/project_readvice/readvice/chatbot/save/chatbot_v50.pth')
                data = [sentence, '0']
                dataset_another = [data]

                another_test = BERTDataset(dataset_another, 0, 1, tok, max_len, True, False)
                test_dataloader = torch.utils.data.DataLoader(another_test, batch_size=batch_size, num_workers=0)

                model.eval()

                for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
                    token_ids = token_ids.long().to(device)
                    segment_ids = segment_ids.long().to(device)

                    valid_length = valid_length
                    label = label.long().to(device)

                    out = model(token_ids, valid_length, segment_ids)
                    # 힘들고 지칠 때 읽을면 좋은 책
                    sad_books = ['나는 나로 살기로 했다', '단상집', '그냥 흘러넘쳐도 좋아요', '아무것도 안 해도 아무렇지 않구나', '죽고 싶지만 떡볶이는 먹고 싶어',
                                 '내가 아무것도 아닐까 봐', '내가 제일 예뻤을 때', '그래도 괜찮은 하루', '서른이면 달라질 줄 알았다', '살면서 쉬웠던 날은 단 하루도 없었다',
                                 '보이지 않는 곳에서 애쓰고 있는 너에게']
                    happy_books = ['불편한 편의점', '어른을 위한 인생수업', '봄이다, 살아보자', '우리는 숲으로 여행간다', '봄의 초대', '입지 센스', '파친코',
                                   '아몬드', '튜브', '모비 딕']
                    angry_books = ['3초간', '나는 오늘부터 화를 끊기로 했다.', '오늘도 욱하셨나요?', '디퓨징', '오늘도 화를 내고 말았습니다', '용서',
                                   '화, 참을 수 없다면 똑똑하게']

                    test_eval = []
                    for i in out:
                        logits = i
                        logits = logits.detach().cpu().numpy()

                        if np.argmax(logits) == 0:  # 화남
                            test_eval.append("마음을 가라앉히고 싶을 때는  ")
                        elif np.argmax(logits) == 1:  # 슬픔
                            test_eval.append("마음의 위로가 필요할 때는  ")
                        elif np.argmax(logits) == 2:  # 행복
                            test_eval.append(" ")

                    if test_eval[0] == "마음을 가라앉히고 싶을 때는  ":
                        print(">> " + test_eval[0] + random.choice(angry_books) + "  라는 책을 읽어보는 건 어떠세요? ")
                    elif test_eval[0] == "마음의 위로가 필요할 때는  ":
                        print(">> " + test_eval[0] + random.choice(sad_books) + "  라는 책을 읽어보는 건 어떠세요?")
                    elif test_eval[0] == " ":
                        print(">> " + test_eval[0] + random.choice(happy_books) + "  라는 책을 읽어보는 건 어떠세요?")
                break


