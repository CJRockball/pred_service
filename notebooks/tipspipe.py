import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, RobustScaler, \
                StandardScaler, OneHotEncoder,FunctionTransformer, PowerTransformer
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from custom_trans import log_transform, func, inverse_func

#Utils
from typing import List
import pathlib
import os
import joblib

ROOT = pathlib.Path(__file__).resolve().parent
PROCESSED_DATA_DIRNAME = ROOT/ "data/processed/split"


class TipsPipe():
    
    def __init__(self):
        
        ## Data
        self.xtrain = pd.read_csv(PROCESSED_DATA_DIRNAME / 'xtrain.csv')
        self.ytrain = pd.read_csv(PROCESSED_DATA_DIRNAME / 'ytrain.csv')
        self.xval = pd.read_csv(PROCESSED_DATA_DIRNAME / 'xval.csv')
        self.yval = pd.read_csv(PROCESSED_DATA_DIRNAME / 'yval.csv')

        if os.path.isfile(PROCESSED_DATA_DIRNAME / 'xtest.csv'):
            self.xtest = pd.read_csv(PROCESSED_DATA_DIRNAME / 'xtest.csv')
            self.test_row = self.xtest.shape[0]
            self.ytest = pd.read_csv(PROCESSED_DATA_DIRNAME / 'ytest.csv')
        
        self.xtrain_pipe = None
        self.xval_pipe = None
        self.xtest_pipe = None
        
        ## Declared variables
        self.cat_name = None
        self.num_name = None
        self.label_name = None

        ## Metadata
        self.random_state = 42
        
        #Pipe
        self.preprocessor = None
        self.trained_pipe = None
    
    def make_preprocessor(self, cat_list: List[str], num_list: List[str], count_list: List[str], pass_list: List[str]) -> None:
        
        l_transformer = FunctionTransformer(log_transform, feature_names_out='one-to-one')
        log_pipeline = Pipeline([('log_tip', l_transformer), ('ss', StandardScaler())])
        
        preprocessor = ColumnTransformer(
            transformers=[('log_nums', log_pipeline,num_list),
                        ('nums', StandardScaler(), count_list), 
                        ('pass','passthrough', pass_list),
                        ('cats', OneHotEncoder(drop='first'), cat_list)])

        self.preprocessor = ('preprocessor',preprocessor)
        return
    
    
    def make_preprocessor2(self, cat_list: List[str], num_list: List[str], count_list: List[str], \
        pass_list: List[str], model) -> None:
         
        # Apply preprocess
        l_transformer = FunctionTransformer(log_transform, feature_names_out='one-to-one')
        log_pipeline = Pipeline([('log_tip', l_transformer), ('ss', StandardScaler())])
        preprocessor = ColumnTransformer(
            transformers=[('log_nums', log_pipeline,num_list),
                        ('nums', StandardScaler(), count_list), 
                        ('pass','passthrough', pass_list),
                        ('cats', OneHotEncoder(drop='first'), cat_list)])

        #Transform data
        pipe = Pipeline(steps=[('preprocessor',preprocessor), 
                            ('classifier', model)])
        tt = TransformedTargetRegressor(regressor=pipe, 
                                        #func=func,
                                        #inverse_func = inverse_func)
                                        transformer=PowerTransformer())
        tt.fit(self.xtrain, self.ytrain)

        self.trained_pipe = tt
        
        return tt
    
    
    def train_pipe(self):
        self.trained_pipe = Pipeline(steps=[self.preprocessor]).fit(self.xtrain)
        return

    def get_preprocessor(self):
        return self.preprocessor
    
    def get_pipe(self):
        return self.trained_pipe
     
    def transform_data(self, data):
        return self.trained_pipe.transform(data)
    
    def get_feature_names(self):
        return self.trained_pipe[:-1].get_feature_names_out()


