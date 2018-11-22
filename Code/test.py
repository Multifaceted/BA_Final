#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 17:58:30 2018

@author: ranger
"""

import pandas as pd
import numpy as np
import os 

os.chdir('/home/ranger/Documents/BA_Project/Code')
from iScrape import *

#raw_data = pd.read_csv('../Data/NYC_Rest_Inspect.csv')
#raw_data['INSPECTION DATE'] = pd.to_datetime(raw_data['INSPECTION DATE'], format = '%m/%d/%Y')
#raw_data['GRADE DATE'] = pd.to_datetime(raw_data['GRADE DATE'], format = '%m/%d/%Y')
#raw_data['RECORD DATE'] = pd.to_datetime(raw_data['RECORD DATE'], format = '%m/%d/%Y')
#data = raw_data[ (raw_data["BORO"] == "MANHATTAN") & (raw_data["CUISINE DESCRIPTION"] == "American") ]

Qitian = pd.read_csv('../Qitian.csv')
fetch_restaurants(Qitian.iloc[ 125 : 150 ])





#fetch_restaurants(Qitian.iloc[[77]])
#np.random.seed(0)
#index = np.random.randint(0, data.shape[0] + 1, size = 1000)
#index2 = np.array(pd.Series(index).drop_duplicates())
#for i in range(140, 145):
#    fetch_restaurants(data.iloc[[index2[i]]])
#
#CAMIS = pd.Series(data['CAMIS'].unique())
#CAMIS_past = data.iloc[index2]['CAMIS']
#not_in_CAMIS_past = CAMIS.apply(lambda x: x not in CAMIS_past.values)
#new = CAMIS[not_in_CAMIS_past]
#expected = new.sample(1000,random_state=0)
#
#df1 = data[data['CAMIS'].apply(lambda x: x in expected.iloc[0:250].values)].groupby(['CAMIS']).first()
#df2 = data[data['CAMIS'].apply(lambda x: x in expected.iloc[250:500].values)].groupby(['CAMIS']).first()
#df3 = data[data['CAMIS'].apply(lambda x: x in expected.iloc[500:750].values)].groupby(['CAMIS']).first()
#df4 = data[data['CAMIS'].apply(lambda x: x in expected.iloc[750:1000].values)].groupby(['CAMIS']).first()
#
#df1.to_csv('Alex.csv')
#df2.to_csv('Lisa.csv')
#df3.to_csv('Weiting.csv')
#df4.to_csv('Qitian.csv')

from gather import *
gather()
