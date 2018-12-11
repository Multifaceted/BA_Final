#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 19:52:21 2018

Script Adapted from Machine Learning Plus 
@author: Qitian Ma
"""

def sent_to_words(sentences):
    from gensim.utils import simple_preprocess
    
    for sentence in sentences:
        yield(simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

def remove_stopwords(texts):
    
    from gensim.utils import simple_preprocess
    from nltk.corpus import stopwords

    stop_words = stopwords.words('english')
    stop_words.extend(["'s"])
    
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(data_words, texts):
    
    from gensim.models import Phrases
    from gensim.models import phrases
    
    bigram = Phrases(data_words, min_count=5, threshold=100)
    bigram_mod = phrases.Phraser(bigram)
    
    return [bigram_mod[doc] for doc in texts]


def lemmatize(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    
    import spacy
    
    nlp = spacy.load('en', disable=['parser', 'ner'])
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        
    return texts_out
