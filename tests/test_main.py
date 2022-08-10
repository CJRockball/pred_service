from fastapi.testclient import TestClient
from api.main import predict
from api.util import predict_test_data
from api.ata_util import get_test_data, get_random_test_row_db
import pytest
from unittest import mock
from unittest.mock import Mock
from fastapi import HTTPException
import numpy as np

client = TestClient(predict)

#---------- main tests ---------------------------
def test_main_root():
    """dummy test"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message':"hello world"}
    
@mock.patch('api.main.get_random_test_row_db')
def test_main_get_random_test_row_mock(mock_get, dummy_dict_list):
    """Test working case"""
    mock_get.return_value = Mock(status_code=200, json=lambda : dummy_dict_list)
    #mock_get.return_value.status_code = 200
    #mock_get.return_value.json = dummy_dict_list
    
    actual = client.get('/get_random_test_row')
    
    expected = dummy_dict_list
    
    assert actual.status_code == 200
    assert actual.json() == expected    
 
 
@mock.patch('api.main.get_random_test_row_db')
def test_main_get_random_test_row_mock_exception(mock_get, dummy_dict_list):
    """Test status code not 200 case"""
    mock_get.return_value = Mock(status_code = 404, json = lambda: dummy_dict_list)

    with pytest.raises(HTTPException) as err:
        client.get('/get_random_test_row')

    assert err.value.status_code == 404
    assert err.value.detail == "Data not found"


@mock.patch('api.main.get_random_test_row_db')
def test_main_get_random_test_row_mock_no_api(mock_get):
    """Test no connection to api"""
    mock_get.return_value = None

    with pytest.raises(HTTPException) as err:
        client.get('/get_random_test_row')

    assert err.value.status_code == 404
    assert err.value.detail == "No connection to API"

        
    
@mock.patch('api.main.get_test_data')
def test_main_get_test_data_mock(mock_get, dummy_dict_list):
    """Test working case"""
    mock_get.return_value = Mock(status_code=200, json=lambda : dummy_dict_list)
    
    actual = client.get('/get_test_data')
    
    expected = dummy_dict_list
    
    assert actual.status_code == 200
    assert actual.json() == expected   
    
# ---------------- util test ------------------------
def test_predict_test_data(dummy_dict_list):
    """Test prediction function"""
    data = dummy_dict_list
    actual = predict_test_data(data)
    
    assert len(actual) == 2
    assert  float(actual['y_pred'])   


# ---------------- data util tests -------------------
@mock.patch('api.main.get_test_data')
def test_data_utils_get_random_test_row_db(mock_get, dummy_dict_list):
    """Test working case"""
    mock_get.return_value = Mock(status_code=200, json=lambda : dummy_dict_list)
    
    actual = client.get('/get_test_data')
    
    expected = dummy_dict_list
    
    assert actual.status_code == 200
    assert actual.json() == expected   