#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 19:37:26 2018

@author: Qitian Ma
"""

def clean_text(text):
    
    import re
    
    text = [sentence.lower() for sentence in text]
    text = [re.sub(r"\s+", " ", sentence) for sentence in text]
    text = [re.sub(r"\\", "", sentence) for sentence in text]
    text = [re.sub(r"([,.!])([^\s])", r"\1 \2",sentence) for sentence in text]
    text = [re.sub(r"that's","that is",sentence) for sentence in text]
    text = [re.sub(r"there's","there is",sentence) for sentence in text]
    text = [re.sub(r"what's","what is",sentence) for sentence in text]
    text = [re.sub(r"where's","where is",sentence) for sentence in text]
    text = [re.sub(r"it's","it is",sentence) for sentence in text]
    text = [re.sub(r"who's","who is",sentence) for sentence in text]
    text = [re.sub(r"i'm","i am",sentence) for sentence in text]
    text = [re.sub(r"i've","i have",sentence) for sentence in text]
    text = [re.sub(r"i'll","i will",sentence) for sentence in text]
    text = [re.sub(r"she'll","she will",sentence) for sentence in text]
    text = [re.sub(r"he'll","he will",sentence) for sentence in text]
    text = [re.sub(r"it'll","it will",sentence) for sentence in text]
    text = [re.sub(r"you'll","you will",sentence) for sentence in text]
    text = [re.sub(r"she's","she is",sentence) for sentence in text]
    text = [re.sub(r"didn't","did not",sentence) for sentence in text]
    text = [re.sub(r"doesn't","does not",sentence) for sentence in text]
    text = [re.sub(r"don't","do not",sentence) for sentence in text]
    text = [re.sub(r"he's","he is",sentence) for sentence in text]
    text = [re.sub(r"they're","they are",sentence) for sentence in text]
    text = [re.sub(r"who're","who are",sentence) for sentence in text]
    text = [re.sub(r"you're","you are",sentence) for sentence in text]
    text = [re.sub(r"ain't","am not",sentence) for sentence in text]
    text = [re.sub(r"wouldn't","would not",sentence) for sentence in text]
    text = [re.sub(r"doesn't","does not",sentence) for sentence in text]
    text = [re.sub(r"shouldn't","should not",sentence) for sentence in text]
    text = [re.sub(r"should've","should have",sentence) for sentence in text]
    text = [re.sub(r"would've","would have",sentence) for sentence in text]
    text = [re.sub(r"can't","can not",sentence) for sentence in text]
    text = [re.sub(r"couldn't","could not",sentence) for sentence in text]
    text = [re.sub(r"let's","let us",sentence) for sentence in text]
    text = [re.sub(r"i'd","i would",sentence) for sentence in text]
    text = [re.sub(r"isn't","is not",sentence) for sentence in text]
    text = [re.sub(r"wasn't","was not",sentence) for sentence in text]
    text = [re.sub(r"weren't","were not",sentence) for sentence in text]
    text = [re.sub(r"won't","will not",sentence) for sentence in text]
    text = [re.sub(r"we're","we are",sentence) for sentence in text]
    text = [re.sub(r"we've","we have",sentence) for sentence in text]
    text = [re.sub(r"hadn't","had not",sentence) for sentence in text]
    text = [re.sub(r"\\*'s"," 's",sentence) for sentence in text]
    return text