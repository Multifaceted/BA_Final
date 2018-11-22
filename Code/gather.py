#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 20:52:14 2018

@author: ranger
"""

def convert_to_sentiment(CAMIS):
    
    """
    Read in the review file of a restaurant identified by CAMIS.
    Drop the reviews with no character.
    Convert each review to a sentiment score using VADER.
    Return the mean of the sentiment scores.
    
    Parameters:
    -----------
    
    TEMPLATE:
    (CAMIS = int/str) -> avg_score = float
    
    INPUT:
    CAMIS: the code of the restaurant
    
    OUTPUT:
    avg_score: the mean of the sentiment scores.
    """
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    import pandas as pd
    
    sid = SentimentIntensityAnalyzer()
    rest = pd.read_csv('../Yelp/' + str(CAMIS) + '.csv', engine = 'python')
    rest.dropna(subset = ['er_text'], inplace = True)
    
    avg_score = rest['er_text'].apply(lambda text: sid.polarity_scores(text)['compound']).mean()
    print(CAMIS)
    
    return avg_score

def gather():
    
    """
    Gather data from NYC_Rest_Inspect.csv', attributes.csv and <CAMIS>.csv, using info.csv as content.
    
    Parameters:
    -----------
    
    TEMPLATE:
    (None) -> None   
    """
    import pandas as pd
    
    info = pd.read_csv('../Yelp/info.csv', usecols = range(1, 6)).drop_duplicates()
    info_aval = info[ info['error_code'].isna() ]  # select observations with no missing data
    info_aval['CAMIS'] = info_aval['CAMIS'].astype(int)
    info_aval = info_aval.drop('error_code', axis = 1)
    
    # Compute the mean sentiment scores of each restaurant.
    info_aval['sentiment_score'] = info_aval['CAMIS'].apply(lambda CAMIS: convert_to_sentiment(CAMIS))
    info_aval.set_index('CAMIS', inplace = True)
    
    # Compute the yearly mean violation scores of inital inspection of each restaurant.
    raw_data = pd.read_csv('../Data/NYC_Rest_Inspect.csv')
    MANHATTAN_American = raw_data[ (raw_data['BORO'] == 'MANHATTAN') & (raw_data['CUISINE DESCRIPTION'] == 'American') ]
    violation_score = MANHATTAN_American[ MANHATTAN_American['INSPECTION TYPE'] == 'Cycle Inspection / Initial Inspection'] \
                        .groupby(['CAMIS', 'INSPECTION DATE'])[ ['SCORE'] ].mean() \
                        .reset_index() \
                        .groupby(['CAMIS'])[ ['SCORE'] ].mean()
    violation_score.rename({'SCORE': 'violation_score'}, axis = 1, inplace = True)
    
    attributes = pd.read_csv('../Yelp/attributes.csv', index_col = 'Unnamed: 0').drop_duplicates()
    
    # Merge Data.
    info_aval = info_aval.join(attributes, how = 'outer') \
                         .join(violation_score, how = 'left')
    
    # Write out aggregated data to csv file.
    info_aval.to_csv('../gathered_data.csv')