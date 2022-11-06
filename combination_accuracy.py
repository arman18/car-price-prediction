# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 15:17:00 2022

@author: arman hossain
"""
from dataset_feature_preprocessor import pre_process
import pandas as pd
from sklearn.linear_model import LinearRegression

def combination(df,category,lastCol):
    
    for col in category:
        category[col] += 1
        idx = category[col]
        # lastCol = category[len(category)-1][0]
        if idx < len(df[col].unique())+1:
            return (category, True)
        else:
            category[col] = 0
            if col == lastCol:
                return (category, False)


if __name__ == '__main__':
    
    data = pd.read_csv('data/original_garibazar_dataset.csv')
    
    data = pre_process(data)
    df =data
    df = df.drop(['Created_date', 'Phone'],axis=1)
    
    category = {'Gearbox':0,'Color':0}
    avail = True
    while avail:
        print(category)
        category,avail = combination(df,category,'Color')
        