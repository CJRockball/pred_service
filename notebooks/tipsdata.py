import pathlib
import pandas as pd
import os

""" Class for data. Loads raw data from source. Splits data in train, val, test"""


ROOT = pathlib.Path(__file__).resolve().parent

DATA_FILENAME = ROOT / "data/tips.csv"
RAW_DATA_FILENAME = ROOT / 'data/raw/tips.csv'
RAW_DATA_DIRNAME = ROOT / 'data/raw/'
PROCESSED_DATA_DIRNAME = ROOT / "data/processed/split"
PROCESSED_DATA_FILENAME = PROCESSED_DATA_DIRNAME / 'tips.csv'

class TipsData():
    """Data class"""
    def __init__(self):
        
        if not os.path.exists(DATA_FILENAME):
            #dl tips data to get mapping
            pass
        
        self.columns = None
        self.lable = None
        self.mapping = None
        self.inverse_mapping = None
        
        self.indims = None
        self.outdims = None
        self.rows = None
        self.train_row = None
        self.val_row = None
        self.test_row = None
        
        self.xy = None
        self.x = None
        self.y = None
        self.xtrain = None
        self.ytrain = None
        self.xval = None
        self.yval = None
        self.xtest = None
        self.ytest = None

    def prepare_data(self, train_split: float = 0.8, val_split: float = 0.1,
                     test_split: float = 0.1, data_shuffle=False) -> None:
        total_data_fractions = train_split + val_split + test_split 
        if total_data_fractions != 1:
            raise ValueError (f'Fractions add to {total_data_fractions} maximum is 1')  
        if not os.path.exists(RAW_DATA_DIRNAME):
            _download_and_process_data()
        if not os.path.exists(PROCESSED_DATA_FILENAME):
            _preprocess_data(train_split, val_split, test_split, data_shuffle)
            
                   
    def setup(self) -> None:
        self.xtrain = pd.read_csv(PROCESSED_DATA_DIRNAME / 'xtrain.csv')
        self.ytrain = pd.read_csv(PROCESSED_DATA_DIRNAME / 'ytrain.csv')
        self.xval = pd.read_csv(PROCESSED_DATA_DIRNAME / 'xval.csv')
        self.yval = pd.read_csv(PROCESSED_DATA_DIRNAME / 'yval.csv')
        self.x = pd.read_csv(PROCESSED_DATA_DIRNAME / 'x.csv')
        self.y = pd.read_csv(PROCESSED_DATA_DIRNAME / 'y.csv')
        self.xy = pd.read_csv(PROCESSED_DATA_DIRNAME / 'xy.csv')
        
        if os.path.isfile(PROCESSED_DATA_DIRNAME / 'xtest.csv'):
            self.xtest = pd.read_csv(PROCESSED_DATA_DIRNAME / 'xtest.csv')
            self.test_row = self.xtest.shape[0]
            self.ytest = pd.read_csv(PROCESSED_DATA_DIRNAME / 'ytest.csv')
        
        self.columns = self.xtrain.columns
        self.lable = self.ytrain.columns
        self.indims = self.xtrain.shape[1]
        self.outdims = self.ytrain.shape[1]
        self.rows = self.xtrain.shape[0] + self.xval.shape[0] + self.xtest.shape[0]
        
        self.train_row = self.xtrain.shape[0]
        self.val_row = self.xval.shape[0]
        
    @classmethod
    def data_dirname(cls):
        """ Returns file path """
        return pathlib.Path(__file__).resolve().parent

    def config(self):
        """ Return important settings of the dataset, which can be passed to model """
        return {'input_dims':self.indims, 'output_dims': self.outdims}
    
    def __repr__(self):
        data_info = f'tips dataset {self.indims}, {self.outdims}, {self.columns}'
        return data_info
    
    def get_train_data(self):
        """ Returns train data subset """
        return self.xtrain, self.ytrain
    
    def get_val_data(self):
        """ Returns val data subset """
        return self.xval, self.yval
    
    def get_raw_data(self):
        """ Returns raw data, feature+label in same df, feature df, label df """
        return self.xy, self.x, self.y
    
    
def _download_and_process_data() -> None:
    """ Checks if data is downloaded otherwise downloads data """
    if not os.path.exists(RAW_DATA_DIRNAME):
        RAW_DATA_DIRNAME.mkdir(parents=True, exist_ok=True)
        
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
    df = pd.read_csv(url)
    
    df.to_csv(RAW_DATA_DIRNAME / 'tips.csv', index=False)
    print(f'Downloading raw dataset from {url}')  
    
    return

    

def _preprocess_data(train_split: float, val_split: float,
                     test_split: float, data_shuffle: bool=False) -> None:
    
    """ Some data preprocessing, splits and saves data """
    
    df = pd.read_csv(RAW_DATA_FILENAME)
        
    #Change col names
    df = df.rename(columns={'size':'g_size'})
    #split data
    #Split of labels
    train_length = int(train_split * df.shape[0])
    val_length = int(val_split * df.shape[0])
    test_length = int(df.shape[0] - (train_length + val_length))
    
    if data_shuffle:
        df = df.sample(frac=1).reset_index(drop=True)
    
    y = df['total_bill']
    x = df.drop(columns='total_bill')
    
    train = df.iloc[:train_length,:]
    ytrain = train['total_bill']
    xtrain = train.drop(columns='total_bill')
    
    d_val = df.iloc[train_length:-test_length, :]
    yval = d_val['total_bill']
    xval = d_val.drop(columns='total_bill')   
    
    test = None        
    if test_length != 0:
        test = df.iloc[test_length:, :]
        ytest = test['total_bill']
        xtest = test.drop(columns='total_bill')           

    #save data artifacts
    if not os.path.exists(PROCESSED_DATA_DIRNAME):
        PROCESSED_DATA_DIRNAME.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(PROCESSED_DATA_DIRNAME / 'xy.csv', index=False)
    x.to_csv(PROCESSED_DATA_DIRNAME / 'x.csv', index=False)
    y.to_csv(PROCESSED_DATA_DIRNAME / 'y.csv', index=False)
    xtrain.to_csv(PROCESSED_DATA_DIRNAME / 'xtrain.csv', index=False)
    ytrain.to_csv(PROCESSED_DATA_DIRNAME / 'ytrain.csv', index=False)
    xval.to_csv(PROCESSED_DATA_DIRNAME / 'xval.csv', index=False)
    yval.to_csv(PROCESSED_DATA_DIRNAME / 'yval.csv', index=False)
    if test is not None:
        xtest.to_csv(PROCESSED_DATA_DIRNAME / 'xtest.csv', index=False)
        ytest.to_csv(PROCESSED_DATA_DIRNAME / 'ytest.csv', index=False)

    return