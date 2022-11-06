# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 15:17:00 2022

@author: arman hossain
"""
from dataset_feature_preprocessor import pre_process
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
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

def get_trin_df(df,category):
    orgdf = df
    for col in category:
        idx = category[col]
        # print(category)
        idx -=1
        if idx < 0:
            df = df[df[col] !=-1]
            continue;
        # print(col, df[col].unique(),idx)
        df = df[df[col] == orgdf[col].unique()[idx]]
    return df

def add_row_to_df(df,accdf,accuracy,category):
    values = [str(accuracy)]
    for col in category:
        idx = category[col]
        idx -=1
        if idx < 0:
            values.append('Any')
            continue;
        values.append(df[col].unique()[idx])
        
    accdf.loc[len(accdf)] = values
    return accdf

def create_empty_df(category):
    obj = {}
    obj["Accuracy"] = []
    for col in category:
        obj[col] = []
    return pd.DataFrame(obj)

# data['Body_type'].unique()

if __name__ == '__main__':
    
    # data = pd.read_csv('data/original_garibazar_dataset.csv')
    
    # data = pre_process(data)
    
    df =data
    df = df.drop(['Created_date', 'Phone'],axis=1)
    
    # ----------- deleting other numeric -------------
    
    # df = df.drop(['Engine', 'Year'],axis=1)
    # numeric = 'Mileage'
    
    # df = df.drop(['Engine', 'Mileage'],axis=1)
    # numeric = 'Year'
    
    # df = df.drop(['Year', 'Mileage'],axis=1)
    # numeric = 'Engine'
    # --------------- end -----------------------------
    
    onlycat = ["Price",'Gearbox','Color','Body_type','Fuel_type','Air_condition','Drive_type','Condition','Model','Location']
    category = {'Gearbox':0,'Body_type':0,'Fuel_type':0,'Air_condition':0,'Drive_type':0,'Condition':0,'Model':0,'Location':0,'Color':0}
    accdf = create_empty_df(category)
    avail = True
    while avail:
        # print(df['Body_type'].unique(),len(df['Body_type'].unique()))
        traindf = get_trin_df(df, category)
        # print(df['Body_type'].unique(),len(df['Body_type'].unique()))
        X = traindf.drop(onlycat, axis=1)
        y = traindf['Price']
        if len(X) > 100:
            X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=10)
            
            lr = LinearRegression()
            lr.fit(X_train,y_train)
            score = lr.score(X_test,y_test)
            accdf = add_row_to_df(df,accdf,score,category)
        category,avail = combination(df,category,'Color')
        