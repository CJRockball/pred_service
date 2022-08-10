from fastapi import FastAPI
from api.main import predict
from fastapi.staticfiles import StaticFiles
import pathlib

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
TEMP_PATH = ROOT_DIR / "templates"
STAT_PATH = ROOT_DIR / "static"


app = FastAPI()
app.mount("/static", StaticFiles(directory=STAT_PATH), name="static")
app.include_router(predict, prefix='/predict', tags=['predict'])