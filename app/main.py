import pathlib
from fastapi import Request, APIRouter, HTTPException, Form
from requests.auth import HTTPBasicAuth
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse, RedirectResponse, HTMLResponse
from typing import Optional
import requests
from os import path
import logging
import starlette.status as status
import httpx
from app.data_util import get_test_data

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
TEMP_PATH = ROOT_DIR / "templates"
STAT_PATH = ROOT_DIR / "static"
templates = Jinja2Templates(directory=TEMP_PATH)
favicon_path = ROOT_DIR / "static/favicon.png"

predict = APIRouter()



@predict.get('/')
def root():
    return {'message':"hello world"}


@predict.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@predict.get("/get_test_data")
async def check_test_data():
    test_data_json = await get_test_data()
    if test_data_json.status_code == 200:
        return test_data_json.json()
    else:
        raise HTTPException(status_code=test_data_json.status_code, detail="Height data not found")

