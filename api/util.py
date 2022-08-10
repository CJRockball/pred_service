import pandas as pd
import joblib
import numpy as np
from  api.custom_trans import log_transform, func, inverse_func
from fastapi import HTTPException

def predict_test_data(json_data):    
    
    df = pd.DataFrame(json_data, columns=['total_bill', 'tip', 'sex', 'smoker', 'day', 'time', 'g_size'])
    
    y_true = df.total_bill
    X = df.drop(columns=['total_bill'])

    l_model = joblib.load('data/model.joblib')

    y_pred = l_model.predict(X.iloc[[0]])
    
    predict_dict = {'y_pred':round(y_pred[0],2), 'y_true':y_true[0]}
    
    return predict_dict

