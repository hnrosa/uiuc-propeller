# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 21:58:40 2023

@author: Heitor Nunes Rosa
@gmail: heitornunes12@gmail.com
@github: @hnrosa
"""

# %%

import xgboost as xgb
from sklearn.model_selection import KFold
from category_encoders import QuantileEncoder
import pandas as pd
import numpy as np
import optuna
import pendulum
import joblib

#%%

df = pd.read_csv('../../data/processed/train.csv')
folds = pd.read_csv('../../data/processed/folds.csv')

kf = KFold(4, shuffle = True, random_state = 101)

folds = [folds.iloc[:, i].dropna() for i in range(folds.shape[1])]

# %%

def objective(trial, approach = 'General', target = 'CT', random = False):
    
    if approach == 'General':
        X = df.loc[:, ['J', 'P_D', 'N']]
    
    elif approach == 'Family':
        X = df.loc[:, ['J', 'P_D', 'N', 'Family']]
        
    elif approach == 'Solidity':
        X = df.loc[:, ['J', 'P_D', 'N', 'Solidity']]
        
    y = df.loc[:, target]
        
    params = {
        'max_depth' : trial.suggest_int('max_depth', 4, 20),
        'min_child_weight' : trial.suggest_int('min_child_weight', 1, 15),
        'learning_rate' : trial.suggest_float('learning_rate', 0.05, 0.2),
        'reg_lambda' : trial.suggest_float('reg_lambda', 1e-6, 1, log = True),
        'reg_alpha' : trial.suggest_float('reg_alpha', 1e-6, 1, log = True),
        'tree_method' : 'hist',
        'n_estimators': 500,
        }
    
    if approach == 'Family':
        quantile = trial.suggest_float('quantile', 0.5, 0.99)
        m = trial.suggest_float('m', 0., 100.)
    
    model = xgb.XGBRegressor(**params)
    
    if approach == 'Family':
        cat_encoder = QuantileEncoder(quantile = quantile, m = m)
        
    evals = []
    
    if random:
        
        for _, fold in kf.split(X):
            
            X_val, y_val = X.loc[fold, :], y.loc[fold]
            X_train, y_train = X.drop(X_val.index), y.drop(y_val.index)
            
            if approach == 'Family':
                cat_encoder.fit(X_train, y_train)
                X_val = cat_encoder.transform(X_val)
                X_train = cat_encoder.transform(X_train)
                
                model.fit(X_train, y_train, eval_set = [(X_val, y_val)], verbose = False)
            
            else:
                model.fit(X_train, y_train, eval_set = [(X_val, y_val)], verbose = False)
                
            eval_result = model.evals_result_['validation_0']['rmse']
            evals.append(eval_result)
            
    else:
        
        for fold in folds:
            
            X_val, y_val = X.loc[fold, :], y.loc[fold]
            X_train, y_train = X.drop(X_val.index), y.drop(y_val.index)
        
            if approach == 'Family':
                cat_encoder.fit(X_train, y_train)
                X_val = cat_encoder.transform(X_val)
                X_train = cat_encoder.transform(X_train)
            
                model.fit(X_train, y_train, eval_set = [(X_val, y_val)], verbose = False)
        
            else:
                model.fit(X_train, y_train, eval_set = [(X_val, y_val)], verbose = False)
            
            eval_result = model.evals_result_['validation_0']['rmse']
            evals.append(eval_result)
    
    evals = np.array(evals)
    avg = evals.mean(axis = 0)
    rmse = avg.min()
    n_estimators = avg.argmin()
    
    trial.set_user_attr('n_estimators', n_estimators)
    
    return rmse

studies = []

for app in ('General', 'Family', 'Solidity'):
    for tg in ('CT', 'CP'):
        obj = lambda trial: objective(trial, approach = app, target = tg)
        study = optuna.create_study(direction = 'minimize')
        study.optimize(obj, n_trials=150)
        studies.append(study)
        
dt = pendulum.now()

date = f'{dt.year}-{dt.month}-{dt.day}_{dt.hour}-{dt.minute}'

i = 0

for obj in ('General', 'Family', 'Solidity'):
    for target in ('CT', 'CP'):
        file = f'studies/{target}_{obj}_study_{date}.joblib'
        with open(file, 'wb') as f:
            joblib.dump(studies[i], f)
            i += 1
            
studies = []
            
for app in ('General', 'Family', 'Solidity'):
    for tg in ('CT', 'CP'):
        obj = lambda trial: objective(trial, approach = app, target = tg, random = True)
        study = optuna.create_study(direction = 'minimize')
        study.optimize(obj, n_trials=150)
        studies.append(study)
        
dt = pendulum.now()

date = f'{dt.year}-{dt.month}-{dt.day}_{dt.hour}-{dt.minute}'

i = 0

for obj in ('General', 'Family', 'Solidity'):
    for target in ('CT', 'CP'):
        file = f'studies/random_{target}_{obj}_study_{date}.joblib'
        with open(file, 'wb') as f:
            joblib.dump(studies[i], f)
            i += 1