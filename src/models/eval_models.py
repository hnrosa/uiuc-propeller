# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 15:32:37 2023

@author: Heitor Nunes Rosa
@gmail: heitornunes12@gmail.com
@github: @hnrosa
"""

from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import mean_squared_error
from category_encoders import QuantileEncoder
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import xgboost as xgb
import pandas as pd
import numpy as np
import joblib

df_train = pd.read_csv('../../data/processed/train.csv')
df_test = pd.read_csv('../../data/processed/test.csv')
folds = pd.read_csv('../../data/processed/folds.csv')

folds = [folds.iloc[:, i].dropna() for i in range(folds.shape[1])]
kf = KFold(4, shuffle = True, random_state = 101)

model_purpose = []
objectives = ('General', 'Family', 'Solidity')
targets = ('CT', 'CP')

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

studies = get_studies('2023-11-4_15-19')
random_studies = get_studies('2023-11-4_16-7', True)

def model_maker(params):
    
    family = 'params_quantile' in params.index
    
    max_depth = params['params_max_depth']
    min_child_weight = params['params_min_child_weight']
    reg_lambda = params['params_reg_lambda']
    reg_alpha = params['params_reg_alpha']
    learning_rate = params['params_learning_rate']
    n_estimators = params['user_attrs_n_estimators']
    
    if family: 
        quantile = params['params_quantile']
        m = params['params_m']

    params = {
        'max_depth' : max_depth,
        'min_child_weight' : min_child_weight,
        'learning_rate' : learning_rate,
        'reg_lambda' : reg_lambda,
        'reg_alpha' : reg_alpha,
        'tree_method' : 'hist',
        'n_estimators': n_estimators,
        }
    
    predictor = xgb.XGBRegressor(**params)
    
    if family: 
        cat_encoder = QuantileEncoder(quantile = quantile, m = m)
        
        model = Pipeline([
            ('encoding', cat_encoder),
            ('predictor', predictor)
            ])
        
    else:
        model = predictor
    
    return model


def eval_studies(studies, random = False):
    
    results = {
        'Train Score': [],
        'CV Score': [],
        'Test Score': [],
        'y_train_pred': [],
        'y_test_pred': [],
        'models': []
        }
    
    for i, (obj, target) in enumerate(model_purpose):
        
        if obj == 'General':
            predictor = ['J', 'P_D', 'N']
        
        elif obj == 'Family':
            predictor = ['J', 'P_D', 'N', 'Family']
            
        elif obj == 'Solidity':
            predictor = ['J', 'P_D', 'N', 'Solidity']
            
        model = model_maker(studies[i])
        
        X_train = df_train.loc[:, predictor]
        y_train = df_train.loc[:, target]
        
        X_test = df_test.loc[:, predictor]
        y_test = df_test.loc[:, target]
        
        if random:
            cv_results = cross_val_score(model, X_train, y_train, cv = kf, 
                            scoring = 'neg_mean_squared_error') * - 1
            
            cv_rmse = np.sqrt(cv_results).mean()
            
        else:
            
            RMSE = []
            
            for fold in folds:
                X_val, y_val = X_train.loc[fold, :], y_train.loc[fold]
                X_par_train, y_par_train = X_train.drop(X_val.index), y_train.drop(y_val.index)
                
                model.fit(X_par_train, y_par_train)
                
                y_pred_val = model.predict(X_val)
                
                rmse = mean_squared_error(y_val, y_pred_val, squared = False)
                
                RMSE.append(rmse)
            
            cv_rmse = np.mean(RMSE)
        
        model.fit(X_train, y_train)
        
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
        
        train_rmse = mean_squared_error(y_train_pred, y_train, squared = False)
        test_rmse = mean_squared_error(y_test_pred, y_test, squared = False)
        
        results['Train Score'].append(train_rmse)
        results['CV Score'].append(cv_rmse)
        results['Test Score'].append(test_rmse)
        results['y_train_pred'].append(y_train_pred)
        results['y_test_pred'].append(y_test_pred)
        results['models'].append(model)
        
        print(f'---Objective: {obj:8s} --- Target: {target:2s}---')
        print(f'TRAIN: {train_rmse:.4f}, CV: {cv_rmse:.4f}, TEST: {test_rmse:.4f}')
        
    return results 

# %%

results = eval_studies(studies)
print('', end = '\n\n')
random_results = eval_studies(random_studies, True)

# %%

fig, ax = plt.subplots(2, 2, figsize = (12, 6), dpi = 300)

indexes = {
    'CT': [0, 2, 4],
    'CP': [1, 3, 5]
    }

def eval_plot(ax, results, target, cv_type):
    
    x = np.arange(3)
    width = 0.25 
    multiplier = 0
    
    for i, (score, value) in enumerate(results.items()):
        
        if i > 2:
            break
        
        ind = indexes[target]
        
        value = np.array(value)[ind]
        
        offset = width * multiplier
        _ = ax.bar(x + offset, value, width, label=score)
        multiplier += 1
        
    ax.set_ylabel('RMSE')
    ax.set_xticks(x + width, objectives) 
    ax.legend(loc='upper left', ncols=3)
    ax.set_title(f'{target} Results by {cv_type} Cross Validation')
    ax.set_ylim(0, .021)
    
eval_plot(ax[0, 0], results, 'CT', 'Custom')
eval_plot(ax[0, 1], random_results, 'CT', 'Random') 
eval_plot(ax[1, 0], results, 'CP', 'Custom')
eval_plot(ax[1, 1], random_results, 'CP', 'Random') 

fig.tight_layout()

#%%

fig, ax = plt.subplots(2, 3, figsize = (15, 6), dpi = 300)

def plot_residuals(axes, results, target):
    
    ind = indexes[target]
    
    y_train_preds = np.array(results['y_train_pred'])[ind, :]
    y_test_preds = np.array(results['y_test_pred'])[ind, :]
     
    y_train = df_train.loc[:, target].to_numpy()
    y_test = df_test.loc[:, target].to_numpy()
    
    y_train_resid = y_train - y_train_preds
    y_test_resid = y_test - y_test_preds
    
    
    for i, ax in enumerate(axes):
        test_score = results["Test Score"][ind[i]]
        train_score = results["Train Score"][ind[i]]
        
        ax.scatter(y_test_preds[i, :], y_test_resid[i, :], alpha = 0.05,
                   color = 'r',
                   label = f'Test Score: {test_score:.3f}')
        ax.scatter(y_train_preds[i, :], y_train_resid[i, :], alpha = 0.05,
                   color = 'b',
                   label = f'Train Score: {train_score:.3f}')
        ax.set_ylim(-0.13, 0.13)
        ax.axhline(0, color = 'k', ls = '--')
        ax.legend(loc = 2)
        ax.set_title(f'{target} {objectives[i]} Residuals')
        ax.set_xlabel('{target} Predictions')
    
ct_axes = (ax[0, 0], ax[0, 1], ax[0, 2])
cp_axes = (ax[1, 0], ax[1, 1], ax[1, 2])
    
plot_residuals(ct_axes, results, 'CT') 
plot_residuals(cp_axes, results, 'CP') 

fig.tight_layout()

#%%

df_test['CT_General'] = results['y_test_pred'][0] 
df_test['CT_Family'] = results['y_test_pred'][2] 
df_test['CT_Solidity'] = results['y_test_pred'][4]  
df_test['CP_General'] = results['y_test_pred'][1] 
df_test['CP_Family'] = results['y_test_pred'][3] 
df_test['CP_Solidity'] = results['y_test_pred'][5] 

def rmse_family(df, target, target_pred):
    y_true = df.loc[:, target]
    y_pred = df.loc[:, target_pred]
    
    return mean_squared_error(y_true, y_pred, squared = False)

df_results = pd.DataFrame()

pd.set_option('display.float_format', '{:.4f}'.format)

for obj, target in model_purpose:
    
    series = df_test.groupby('Family').apply(
        lambda df: rmse_family(df, f'{target}', f'{target}_{obj}')
        )
    
    df_results[f'{target}_{obj}'] = series
    
df_results['Counts'] = df_test.groupby('Family').size()
    
print(df_results)
