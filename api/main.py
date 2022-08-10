import pathlib
from fastapi import APIRouter, HTTPException
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from typing import Optional
import logging
from api.data_util import get_test_data, get_random_test_row_db
from api.util import predict_test_data


ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
TEMP_PATH = ROOT_DIR / "templates"
STAT_PATH = ROOT_DIR / "static"
templates = Jinja2Templates(directory=TEMP_PATH)
favicon_path = ROOT_DIR / "static/favicon.png"
LOG_FILE = ROOT_DIR / "logs/info.log"

logging.basicConfig(
    filename=LOG_FILE,
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
)


predict = APIRouter()


@predict.get('/')
def root():
    return {'message':"hello world"}


@predict.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@predict.get("/get_test_data")
async def check_test_data():
    logging.info("Getting all test data")
    test_data_json = await get_test_data()
    
    if test_data_json is None:
        raise HTTPException(status_code=404, detail="No connection to API")
    
    if test_data_json.status_code == 200:
        return test_data_json.json()
    else:
        raise HTTPException(status_code=test_data_json.status_code, detail="Data not found")


@predict.get("/get_random_test_row")
async def get_random_test():
    logging.info("Getting random row of test data")
    test_data_json = await get_random_test_row_db()

    if test_data_json is None:
        raise HTTPException(status_code=404, detail="No connection to API")

    if test_data_json.status_code == 200:
        return test_data_json.json()
    else:
        raise HTTPException(status_code=test_data_json.status_code, detail="Data not found")
    

@predict.get("/get_test_prediction")
async def get_random_test():
    logging.info("Make prediction on random row of test data")
    return_data = await get_random_test_row_db()
    return_json = return_data.json()
    
    if return_data is None:
        raise HTTPException(status_code=404, detail="No connection to API")

    if return_data.status_code == 200:
        pred_dict = predict_test_data(return_json)
        return pred_dict
    else:
        raise HTTPException(status_code=return_data.status_code, detail="Data not found")
    

    