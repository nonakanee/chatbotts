#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np
import tflearn
#import tensorflow as tf
import tensorflow.compat.v1 as tf
import random
import json
import pickle
import codecs
from attacut import tokenize

#with open("intents.json",encoding="utf8") as file:
with open("intents_th.json",encoding="utf8") as file:
    data = json.load(file)

try:
    with open("data_th.pickle","rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    ##################################################
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            #wrds = nltk.word_tokenize(pattern)#EN
            wrds = tokenize(pattern)#TH
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)


    training = np.array(training)
    output = np.array(output)
    ##################################################

    with open("data_th.pickle","wb") as f:
        pickle.dump((words, labels, training, output), f)

tf.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

#Train
#model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
#model.save("model.tflearn")

try:
    model.load("model.tflearn")
except:
    #######################################################
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")
    #######################################################

def clean_text(wd):
    #remove pynctuation
    wd = wd.transslate(str.maketrans('',''.string.punctuation))
    #convert to lower case
    wd = wd.lower()
    return wd

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    #print(words)#data train

    #s_words = nltk.word_tokenize(s)#EN
    s_words = tokenize(s)#TH
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)

def chat(massage):
#def chat():
    print("Start talking with the bot (type quit to stop)!")
    while True:
        #inp = input("You: ")
        inp = massage
        if inp.lower() == "quit":
            break

        results = bag_of_words(inp, words)
        #print(results)
        kv = np.sum(results)#kv = Khowledge Value

        results = model.predict([bag_of_words(inp, words)])
        results_index = np.argmax(results)
        tag = labels[results_index]

        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        if kv > 0:
            #print(random.choice(responses))
            return random.choice(responses)
        else:
            msg = 'ตอนนี้ บอทนิ อยู่ระหว่างพัฒนาใน version 1 ยังเรียนรู้ไม่พอครับ อาจไม่เข้าใจที่สื่อสาร บอทนิ ขออนุญาตเก็บรวบรวมคำถามไว้นะครับ เพื่อใช้พัฒนาตัวเอง คิดว่าไม่นาน บอทนิ จะสามารถตอบคำถามนี้ได้แน่นอนครับ'
            #print(msg)
            return msg

#chat()