# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 15:16:13 2022

@author: arman hossain
"""

import pandas as pd

data = pd.read_csv('data/original_garibazar_dataset.csv')
''' 
['web-scraper-order', 'web-scraper-start-url', 'container',
       'container-href', 'price', 'created_date', 'Phone', 'Engine', 'Gearbox',
       'Mileage', 'Year', 'Color', 'Body_type', 'Fuel_type', 'Air_condition',
       'Drive_type', 'Condition', 'Model', 'Location']

'''

def shift_right(data,idx):
    arr = ['Mileage','Year','Color','Body_type','Fuel_type','Air_condition','Drive_type','Condition']
    n = len(arr)-1
    while n > 0:
        data[arr[n]][idx] = data[arr[n-1]][idx]
        n-=1
    data['Mileage'][idx] = -1
    
def shift_data_right(data, col='Mileage'):
    
    for idx in range(len(data[col])):
        val = data['Mileage'][idx]
        if val.find("Year") == 0:
            shift_right(data,idx)

# 1 Shift if neccessary
shift_data_right(data)


def process_price(data):
    col = 'Price'
    for idx in range(len(data[col])):
        price = data[col][idx]
        if price == 'NEGOTIABLE':
            data[col][idx] = -1
            continue
        value = ''.join(i for i in price if i.isdigit())
        data[col][idx] = int(value)
    
    data = data[data[col]!=-1]
    data = data.reset_index(drop=True)
    return data
    
# 2 Price processing
data = process_price(data)


def remove_prepend_string(data,col):
    
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
data2 = data
arr = [('Engine',6),('Color',5),('Year',4),('Mileage',7),('Gearbox',7),('Body_type',9),
       ('Fuel_type',9),('Air_condition',7),('Drive_type',10), ('Condition',9)]
# remove_prepend_string(data, arr[0])
for item in arr:
    remove_prepend_string(data, item)


# 4 make N/A to -1

for col in data:
    for idx in range(len(data[col])):
        val = data[col][idx]
        if val == 'N/A': data[col][idx] = -1
        
# Remove unit comma
arr = ['Engine','Mileage']
for col in arr:
    for idx in range(len(data[col])):
        value = data[col][idx]
        if value == -1: continue
        nvalue = ''.join(i for i in value if i.isdigit())
        data[col][idx] = int(nvalue)