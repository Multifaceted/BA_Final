#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 19:35:14 2018

Script Adapted from Machine Learning Plus 
@author: Qitian Ma
"""

def LDA(text):
    
    from gensim.models import ldamodel    
    from clean_text import clean_text
    from LDA_AuxFunc import sent_to_words, remove_stopwords, make_bigrams, lemmatize
    
    import gensim.corpora as corpora
    
    import warnings
    import logging
    
    
    logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.ERROR)
    warnings.filterwarnings("ignore", category = DeprecationWarning)

    text = clean_text(text)
    
    data_words = list(sent_to_words(text))
    
    data_words_nostops = remove_stopwords(data_words)
    
    data_words_bigrams = make_bigrams(data_words, data_words_nostops)
    
    data_lemmatized = lemmatize(data_words_bigrams, allowed_postags = ['NOUN', 'ADJ', 'VERB', 'ADV'])
    
    id2word = corpora.Dictionary(data_lemmatized)
    
    corpus = [id2word.doc2bow(text) for text in data_lemmatized]
    
    lda_model = ldamodel.LdaModel(corpus = corpus,
                                  id2word = id2word,
                                  num_topics = 3, 
				  random_state = 1,
                                  update_every = 1,
                                  chunksize = 50,
                                  passes = 20,
                                  alpha = 'auto',
                                  per_word_topics = True)
    
    return (lda_model, corpus, id2word)
