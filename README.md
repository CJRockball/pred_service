# Prediction Demo
This project is looking at the tips dataset. The goal is to predict a waiter's tip. It can be found [here](https://www.kaggle.com/code/sanjanabasu/tips-dataset/data). It's a very small dataset with 243 entries. It has continuous and categorical(nominal and ordinal) features and it has a continuous label, so it's a regression problem. However, it turns out only one feature is needed for the tip prediction, so let's try to explain the total_bill price instead.

## Outline
- Background
- Coding components, sklearn lin red, notebooks, mlflow, rmdbs, pytest, 
- Site Overview
- Comment on training
- Comment on db
- Comment on pytest
- Comment on deploying, fastapi
- Run

## Background


## Coding Components
### Folder layout
### Notebooks - EDA and Training
### Serving - Heroku and FastAPI


## Site Overview


## Comment on Training


## Comment on db


## Comment on pytest


## Comment on Deploying, FasrtAPI

## Run
# Run from File
* Clone the db_service repo
* Run database. In the terminal, got to the database folder. Run `uvicorn api.router:app --reload --port 8001`
* Open browser at `127.0.0.1:8001/tips/`. The response will be "message: hello world tips" to confirm that it works.
* Clone pred_service repo
* Open the data_util file in the api folder. Change the clients to the host.docker ones
* In a terminal go to folder and run `uvicorn api.router:app --reload`
* Open a browser window at `127.0.0.1:8000/predict/`. The response will be "meassage: Hello world" to confirm that it works.

### To Run from Docker
* Clone the db_service repo
* Change the last line in the Dokerfile, commnet the current CMD line and uncomment the above CMD line
* In a terminal go to folder and run `docker build -t name .` 
* Then run `docker run -dp 8001:8001 name`
* Open browser at `127.0.0.1:8001/tips/`. The response will be "message: hello world tips" to confirm that it works.
* Clone pred_service repo
* Change the last line in the Dokerfile, commnet the current CMD line and uncomment the above CMD line
* In a terminal go to folder and run `docker build -t name .` 
* Then run `docker run -dp 8000:8000 name`
* Open browser at `127.0.0.1:8000/predict/`. The response will be "message: Hello world" to confirm that it works.
