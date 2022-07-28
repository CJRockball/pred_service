import httpx
#import requests
#import os
#from config.config_utils import load_config

#config = load_config("config_file.yaml")
#adr = config['data_source']

# CAST_SERVICE_HOST_URL = 'http://host.docker.internal:8002'
# url = os.environ.get('DATA_SERVICE_HOST_URL') or CAST_SERVICE_HOST_URL
# "http://baby-j-data-service.herokuapp.com/api/v1/datas/" # "http://127.0.0.1:8000/api/v1/datas/"  #   "http://data_service:8000/api/v1/datas/" #  

async def get_test_data():
    # w_json = requests.get("http://host.docker.internal:8000/weight")
    #data_json = requests.get("http://127.0.0.1:8000/weight")
    #w_json = httpx.get(adr + "weight")
    print('hej')
    async with httpx.AsyncClient() as client:
        w_json = await client.get("http://127.0.0.1:8001/tips/test_data")
    return w_json