# -*- coding: utf-8 -*-
import csv
import os
import re

import pandas as pd
import torch
from scipy.spatial.distance import cosine
from transformers import BertTokenizer, BertModel


tokenizer = BertTokenizer.from_pretrained(
    r'D:\courses\juniorsec\social_network\lab\final\bert_model\PyTorch_version')
model = BertModel.from_pretrained(r'D:\courses\juniorsec\social_network\lab\final\bert_model\PyTorch_version')


def getAnswer(context, question):
    try:
        # 将上下文分成句子
        sentences = context.split('。')
        # 对每个句子进行编码
        sentence_embeddings = []
        for sentence in sentences:
            if len(sentence) > 0:
                inputs = tokenizer(sentence, return_tensors="pt")
                with torch.no_grad():
                    outputs = model(**inputs)
                sentence_embeddings.append(outputs.last_hidden_state[0].mean(dim=0))

        # 对问题进行编码
        inputs = tokenizer(question, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
        question_embedding = outputs.last_hidden_state[0].mean(dim=0)

        # 计算问题和每个句子的相似度
        similarities = []
        for sentence_embedding in sentence_embeddings:
            similarity = 1 - cosine(sentence_embedding, question_embedding)
            similarities.append(similarity)

        # 选择最相似的句子作为答案
        most_similar_index = similarities.index(max(similarities))
        answer = sentences[most_similar_index]
        print(f"Answer: {answer}")
    except Exception:
        answer = ""
    return answer


template = [
    '{}采取了什么措施来帮助毕业生就业',
    '为了帮助毕业生就业，{}采取了什么措施',
    '为了帮助毕业生就业，{}做了什么',
    '{}给毕业生提供哪些帮助',
    '{}给毕业生提供哪些支持',
    '在{}有哪些帮助毕业生就业的政策',
    '在{}有哪些帮助毕业生的政策',
    '在{}的毕业生可以获得哪些帮助',
    '在{}有哪些政策可以促进毕业生就业',
    '{}为毕业生提供了哪些就业指导服务',
    '{}政府如何促进毕业生就业',
    '{}政府如何帮助毕业生解决就业难题',
]

butie_templates = [
    '{}给就业的毕业生提供哪些补贴',
    '在{}就业的毕业生可以获得多少补贴',
    '在{}就业的毕业生可以获得多少补贴',
    '{}政府为毕业生提供了哪些补贴',
]

keywords = ['补贴', '优惠', '支持', '援助', '补助', '措施', '享受', '收费', '免收', '发放']

folder_path = 'D:\\courses\\juniorsec\\social_network\\lab\\final\\code\\Policy\\csv'

# 生成问答对
# 初始化
with open('D:\\courses\\juniorsec\\social_network\\lab\\final\\code\\Policy\\qa.csv', 'a', encoding='utf_8_sig', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["question"] + ["answer"] + ["province"] + ["date"] + ["html"])
for filename in os.listdir(folder_path):
    province = filename.split('.')[0]
    dataFrame = []
    file_path = os.path.join(folder_path, filename)
    data = pd.read_csv(file_path, encoding='utf_8_sig')
    #删除内容为空的行
    #data = data[data['内容'].notna()]
    #删除重复的行
    #data = data.drop_duplicates()
    text = data['内容']
    for i in range(len(text)):
        question = template[i % len(template)].format(province)
        context = ""
        line = str(text[i])
        delimiters = "。？！."
        sentences = re.split('|'.join(map(re.escape, delimiters)), line)
        for sentence in sentences:
            if "毕业生" not in sentence or "大学生" not in sentence:
                continue
            for keyword in keywords:
                if keyword in sentence:
                    if keyword == '补贴':
                        question = butie_templates[i % len(butie_templates)].format(province)
                    context = context + str(sentence) + '。'
                    break
        answer = getAnswer(context, question)

        # 写入question+answer等
        if answer != "":
            with open('D:\\courses\\juniorsec\\social_network\\lab\\final\\code\\Policy\\qa.csv', 'a', encoding='utf_8_sig', newline='') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
                writer.writerow([question] + [answer] + [province] + [data.iloc[i][0]] + [data.iloc[i][1]])