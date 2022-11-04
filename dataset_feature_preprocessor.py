# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 15:16:13 2022

@author: arman hossain
"""

import pandas as pd

data = pd.read_csv('data/original_garibazar_dataset.csv')
''' 
['web-scraper-order', 'web-scraper-start-url', 'container',
       'container-href', 'price', 'created_date', 'GearBox', 'Milage', 'Year',
       'Color', 'Body_type', 'fuel_type', 'Air_Con', 'DriveType', 'Condition',
       'contact']

'''
# price processing

for idx in range(len(data['price'])):
    price = data['price'][idx]
    if type(price) != str:
        data['price'][idx] = -1
        continue
    value = ''.join(i for i in price if i.isdigit())
    data['price'][idx] = int(value)

data = data[data['price']!=-1]

# Milage processing