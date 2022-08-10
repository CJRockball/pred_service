import httpx
#from config.config_utils import load_config

#config = load_config("config_file.yaml")
#adr = config['data_source']

# CAST_SERVICE_HOST_URL = 'http://host.docker.internal:8002'
# url = os.environ.get('DATA_SERVICE_HOST_URL') or CAST_SERVICE_HOST_URL
# "http://baby-j-data-service.herokuapp.com/api/v1/datas/" # "http://127.0.0.1:8000/api/v1/datas/"  #   "http://data_service:8000/api/v1/datas/" #  

async def get_test_data():
    async with httpx.AsyncClient() as client:
        try:
            data_json = await client.get("http://127.0.0.1:8001/tips/test_data")
            return data_json
        except httpx.RequestError as exc:
            print(f'An error occurred while requesting {exc.request.url!r}.')

async def get_random_test_row_db():
    async with httpx.AsyncClient() as client:
        try:
            data_json = await client.get("http://127.0.0.1:8001/tips/get_random_test_data")
            return data_json
        except httpx.RequestError as exc:
            print(f'An error occurred while requesting {exc.request.url!r}.')

    