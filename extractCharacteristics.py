# -*- coding: utf-8 -*-
"""
Based on code from Jordy Thielen
Extracts characteristics from folk music from the Music21 corpus, and saves these characteristics in a csv file
"""
import numpy as np
import generator
import os
import csv

## Variables/Parameters 
modelType = 'secondOrder'    #existing model types: 'flat', 'firstOrder', TODO: create: 'secondOrder', 'prior', 'start', 'end'
dataSet = 'essenFolk'            #'allFolk', 'folk', 'essenFolk', 'bach'
directory = 'data\\'+dataSet+'\\'+modelType+'\\'

if not os.path.exists(directory):
    os.makedirs(directory)

## Generate specified frequency data for the specified dataset
gen = generator.Generator(modelType, dataSet)
distribution = gen.generateDistribution()

# Write data to csv file
csvfile = directory+'distribution.csv'
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(distribution)

csvfile= directory+'distribution.csv'
with open (csvfile) as csvin:
    x = csv.reader(csvin)
    y = np.asarray([list(map(float, z)) for z in x])
