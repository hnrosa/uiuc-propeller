# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 15:53:05 2023

@author: Heitor Nunes Rosa
@gmail: heitornunes12@gmail.com
@github: @hnrosa
"""
import pandas as pd

df = pd.read_csv('../../data/processed/data.csv')

ind = df.query('Blade > 2').index

df = df.drop(ind)

props = df[['Family', 'PropName']].drop_duplicates()

values = props['Family'].value_counts()

test_props = []

for value, ind in zip(values, values.index):
    
    if value > 1:
        
        props_ = props.loc[props['Family'] == ind, 'PropName']
        
        props_ = props_.sample(frac = 1, random_state = 500)
        
        test_p = props_.iloc[0:int(value * 0.2) + 1]
        
        test_props.append(test_p)
        
test_props = pd.concat(test_props)


test_index = df['PropName'].isin(test_props)
train_index = ~test_index

test_data = df.loc[test_index, :] 
train_data = df.loc[train_index, :]

train_props = train_data['PropName'].drop_duplicates()

train_props = train_props.sample(frac = 1, random_state = 101)

prop_folds = [train_props[i*45:(i+1)*45] for i in range(4)]

miss_prop = df['PropName'] == train_props.iloc[-1]

test_data = pd.concat([test_data, train_data.loc[miss_prop, :]])

train_data = train_data.drop(train_data.loc[miss_prop, :].index)

folds = []

for prop_fold in prop_folds:
    fold_index = train_data['PropName'].isin(prop_fold)
    folds.append(fold_index)
        
folds = pd.concat(folds, axis = 1)

train_data.to_csv('../../data/processed/train.csv', index = False)
test_data.to_csv('../../data/processed/test.csv', index = False)
folds.to_csv('../../data/processed/folds.csv', index = False)


print(f'Not Null Train: {train_data["Solidity"].notnull().sum():5d} Instances')
print(f'Is Null Train:  {train_data["Solidity"].isnull().sum():5d} Instances')
print(f'Not Null Test:  {test_data["Solidity"].notnull().sum():5d} Instances')
print(f'Is Null Test:   {test_data["Solidity"].isnull().sum():5d} Instances')

