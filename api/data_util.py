import httpx

async def get_test_data():
    async with httpx.AsyncClient() as client:
        try:
            data_json = await client.get('http://db-data-service.herokuapp.com/tips/test_data/') #'http://host.docker.internal:8001/tips/test_data/') #"http://127.0.0.1:8001/tips/test_data") #
            return data_json
        except httpx.RequestError as exc:
            print(f'An error occurred while requesting {exc.request.url!r}.')

async def get_random_test_row_db():
    async with httpx.AsyncClient() as client:
        try:
            data_json = await client.get('http://db-data-service.herokuapp.com/tips/get_random_test_data/') #http://host.docker.internal:8001/tips/get_random_test_data') #"http://127.0.0.1:8001/tips/get_random_test_data") #
            return data_json
        except httpx.RequestError as exc:
            print(f'An error occurred while requesting {exc.request.url!r}.')

    