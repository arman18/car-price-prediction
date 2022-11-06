# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 15:16:13 2022

@author: arman hossain
"""

import pandas as pd


def _remove_missing_instances(data,col,value=-1):
    data = data[data[col]!=value]
    data = data.reset_index(drop=True)
    return data

def _shift_right(data,idx):
    arr = ['Mileage','Year','Color','Body_type','Fuel_type','Air_condition','Drive_type','Condition']
    n = len(arr)-1
    while n > 0:
        data[arr[n]][idx] = data[arr[n-1]][idx]
        n-=1
    data['Mileage'][idx] = -1
    
def _shift_data_right(data, col='Mileage'):
    
    for idx in range(len(data[col])):
        val = data['Mileage'][idx]
        if val.find("Year") == 0:
            _shift_right(data,idx)

# 1 Shift if neccessary
# shift_data_right(data)


def _process_price(data):
    col = 'Price'
    for idx in range(len(data[col])):
        price = data[col][idx]
        if price == 'NEGOTIABLE':
            data[col][idx] = -1
            continue
        value = ''.join(i for i in price if i.isdigit())
        data[col][idx] = int(value)
    return _remove_missing_instances(data, col,-1)


# 2 Price processing
# data = process_price(data)


def _remove_prepend_string(data,col):
    
    start = col[1]
    col = col[0]
    # print(start)
    for idx in range(len(data[col])):
        # print(idx,data[col])
        if type(data[col][idx]) != str:
            data[col][idx] = -1
            continue
        data[col][idx] = data[col][idx][start:]
    # print(data[col].unique())



# 3 Remove prepend string
# data2 = data
# arr = [('Engine',6),('Color',5),('Year',4),('Mileage',7),('Gearbox',7),('Body_type',9),
#        ('Fuel_type',9),('Air_condition',7),('Drive_type',10), ('Condition',9)]
# # remove_prepend_string(data, arr[0])
# for item in arr:
#     remove_prepend_string(data, item)


# 4 make N/A to -1
def _change_na(data):
    for col in data:
        for idx in range(len(data[col])):
            val = data[col][idx]
            if val == 'N/A': data[col][idx] = -1
        
# Remove unit comma and make integer
def _remove_extra_string(data):
    arr = ['Engine','Mileage','Year']
    for col in arr:
        for idx in range(len(data[col])):
            value = data[col][idx]
            if value == -1: continue
            nvalue = ''.join(i for i in value if i.isdigit())
            data[col][idx] = int(nvalue)
        
# created date
def _change_create_date(data):
    
    dates = {"January":'01','February':'02','March':'03','April':'04','May':'05','June':'06','July':'07','August':'08',
             'September':'09','October':'10','November':'11','December':'12'}
    col = 'Created_date'
    flag = False
    for idx in range(len(data[col])):
        # print(idx,data[col][idx])
        if str(data[col][idx]) == 'nan':
            data[col][idx]= -1
            continue
        date = data[col][idx].split(" ")
        
        ndate=""
        if date[0]=="December": flag = True
        if flag== True and date[0]!='December':
            ndate = date[1]+'-'+dates[date[0]]+'-2022'
        else: ndate = date[1]+'-'+dates[date[0]]+'-2021'
        data[col][idx] = ndate
    
def make_upper_case(data):
    cols = ['Gearbox','Color','Body_type','Fuel_type','Air_condition','Drive_type','Condition','Model','Location']
    for item in cols:
        data[item] = data[item].str.upper()
def fill_average(df):
    cols = ['Engine','Mileage','Year']
    for col in cols:
        for idx in range(len(df)):
            if df[col][idx]==-1:
                total = 0
                cnt = 0
                for i in range(idx+1,len(df)):
                    if df[col][i] != -1:
                        cnt+=1
                        total += df[col][i]
                    if cnt==15:
                        df[col][idx] = int(total/cnt)
                        break
                if cnt!=15:
                    for i in range(idx-15+cnt,idx):
                        cnt+=1
                        total += df[col][i]
                    df[col][idx] = int(total/cnt)
# data.head()
def pre_process(data):
    
    _shift_data_right(data)
    data = _process_price(data)
    
    arr = [('Engine',6),('Color',5),('Year',4),('Mileage',7),('Gearbox',7),('Body_type',9),
           ('Fuel_type',9),('Air_condition',7),('Drive_type',10), ('Condition',9)]
    # remove_prepend_string(data, arr[0])
    for item in arr:
        _remove_prepend_string(data, item)
    _change_na(data)
    _remove_extra_string(data)
    _change_create_date(data)
    data = data.drop(['web-scraper-order', 'web-scraper-start-url', 'container','container-href'], axis=1)
    make_upper_case(data)
    fill_average(data)
    
    return data

# data.to_csv('preprocessed.csv',index=False)

if __name__ == '__main__':
    data = pd.read_csv('data/original_garibazar_dataset.csv')
    data = pre_process(data)
    
    
