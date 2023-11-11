# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 02:23:42 2023

@author: Heitor Nunes Rosa
@gmail: heitornunes12@gmail.com
@github: @hnrosa
"""

from category_encoders import QuantileEncoder
import xgboost as xgb
import pandas as pd
import numpy as np
import joblib

df = pd.read_csv('../../data/processed/train.csv')

model_purpose = []
objectives = ('General', 'Family', 'Solidity')
targets = ('CT', 'CP')
date = '2023-11-4_15-19'

for obj in objectives:
    for target in targets:
        model_purpose.append((obj, target))
        
def get_studies(date, random = ''):

    studies = []
    
    if random:
        random = 'random_'
    
    for obj, target in model_purpose:
        file = f'studies/{random}{target}_{obj}_study_{date}.joblib'
        study = joblib.load(file)
        study = study.trials_dataframe().sort_values(by = 'value')
        studies.append(study.iloc[0, :])
        
    return studies    

studies = get_studies(date)

def model_maker(params, X, y):
    
    family = 'params_quantile' in params.index
    
    max_depth = params['params_max_depth']
    min_child_weight = params['params_min_child_weight']
    reg_lambda = params['params_reg_lambda']
    reg_alpha = params['params_reg_alpha']
    learning_rate = params['params_learning_rate']
    n_estimators = params['user_attrs_n_estimators']
    alphas = np.array([0.05, 0.95])
    
    if family: 
        quantile = params['params_quantile']
        m = params['params_m']
        cat_encoder = QuantileEncoder(quantile = quantile, m = m)
        cat_encoder.fit(X, y)
        X[:, 3] = cat_encoder.transform(X).to_numpy()[:, 3]
        
    Xy = xgb.DMatrix(X, y)

    params_quantiles = {
        'objective': 'reg:quantileerror',
        'quantile_alpha': alphas, 
        'max_depth' : max_depth,
        'min_child_weight' : min_child_weight,
        'learning_rate' : learning_rate,
        'reg_lambda' : reg_lambda,
        'reg_alpha' : reg_alpha,
        'tree_method' : 'hist',
        }
    
    params = {
        'max_depth' : max_depth,
        'min_child_weight' : min_child_weight,
        'learning_rate' : learning_rate,
        'reg_lambda' : reg_lambda,
        'reg_alpha' : reg_alpha,
        'tree_method' : 'hist',
        }
    
    xgb_model_mean = xgb.train(params, Xy, n_estimators)
    xgb_model_quantiles = xgb.train(params_quantiles, Xy, n_estimators)
    
    if family:
        
        return (xgb_model_mean, xgb_model_quantiles, cat_encoder)
    
    else:
        return (xgb_model_mean, xgb_model_quantiles)
    
    
for i, (obj, target) in enumerate(model_purpose):
    
    if obj == 'General':
        predictor = ['J', 'P_D', 'N']
    
    elif obj == 'Family':
        predictor = ['J', 'P_D', 'N', 'Family']
        
    elif obj == 'Solidity':
        predictor = ['J', 'P_D', 'N', 'Solidity']
        
    X_train = df.loc[:, predictor].to_numpy()
    y_train = df.loc[:, target].to_numpy()
        
    models = model_maker(studies[i], X_train, y_train)
    
    if len(models) > 2:
        joblib.dump(models[0], f'../../models/{target}_{obj}_model_{date}.joblib')
        joblib.dump(models[1], f'../../models/{target}_{obj}_model_quantile_{date}.joblib')
        joblib.dump(models[2], f'../../models/{target}_{obj}_encoder_{date}.joblib')
        
    else:
        joblib.dump(models[0], f'../../models/{target}_{obj}_model_{date}.joblib')
        joblib.dump(models[1], f'../../models/{target}_{obj}_model_quantile_{date}.joblib')
        
    print(f'{target}_{obj} done.')
        




