import sqlite3
import pathlib
import pandas as pd
import numpy as np

PROJECT_PATH = pathlib.Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_PATH / "data/new_tips.db"

def get_db_data():
    global DB_PATH
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        cur.execute("SELECT bill_prediction, tip, sex, smoker, day, time,g_size FROM new_data_table;")
        result = cur.fetchall()
        df = pd.DataFrame(result, columns=['bill_prediction', 'tip', 'sex', 'smoker', 'day', 'time', 'g_size'])
        
        return df
    
    
def tuplefy(df):
    data_tmp = [tuple(x[:]) for x in df.to_numpy()]
    data_tuple = tuple(data_tmp[0])
    return data_tuple

def write_data(df_data):
    data_tuple = tuplefy(df_data)

    #print(">>>>Writing to DB")
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO new_data_table (bill_prediction, tip, sex, smoker, day, time, g_size) VALUES (?,?,?,?,?,?,?);" "", data_tuple)
        
    #print('>>>> Done')
    return 

if __name__ == "__main__":
    #Test load data into database
    test_data = np.array([15.00, 3.45, 'Male', 'No', 'Fri', 'Dinner', 3]).reshape(1,7)
    df_test_data = pd.DataFrame(data=test_data, columns=['bill_prediction', 'tip', 'sex', 'smoker', 'day', 'time', 'g_size'])
    write_data(df_test_data)