import pandas as pd
import pytest

@pytest.fixture()
def dummy_dict_list():
    return [{'total_bill':12.6, 'tip':1, 'sex':"Male", 'smoker':'Yes', 'day':'Sat', 'time':'Dinner', 'g_size':2}]

@pytest.fixture()
def dummy_df():
    result = [(12.6, 1, "Male", 'Yes', 'Sat', 'Dinner', 2)]
    df = pd.DataFrame(result, columns=['total_bill', 'tip', 'sex', 'smoker', 'day', 'time', 'g_size'])
    return df