import pandas as pd
import joblib
import json
import numpy as np
from  api.custom_trans import log_transform, func, inverse_func
from api.db_utils import write_data
from fastapi import HTTPException

def predict_test_data(json_data):    
    """ Function to predict new total bill """
    df = pd.DataFrame(json_data, columns=['total_bill', 'tip', 'sex', 'smoker', 'day', 'time', 'g_size'])
    
    y_true = df.total_bill
    X = df.drop(columns=['total_bill'])

    l_model = joblib.load('data/model.joblib')

    y_pred = l_model.predict(X.iloc[[0]])
    
    predict_dict = {'y_pred':round(y_pred[0],2), 'y_true':y_true[0]}
    
    return predict_dict

def db_load(json_data, pred_dict):
    """ Function to load data in database"""
    data_dict = json_data[0]
    del data_dict['total_bill']
    
    data_dict['bill_prediction'] = pred_dict['y_pred']
    df = pd.DataFrame([data_dict], columns=['tip', 'sex', 'smoker', 'day', 'time', 'g_size','bill_prediction'])
    
    write_data(df)
    
    return
    
