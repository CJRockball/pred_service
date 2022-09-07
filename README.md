# Prediction Demo
This project is looking at the tips dataset. The goal is to predict a waiter's tip. It can be found [here](https://www.kaggle.com/code/sanjanabasu/tips-dataset/data). It's a very small dataset with 243 entries. It has continuous and categorical(nominal and ordinal) features and it has a continuous label, so it's a regression problem. However, it turns out only one feature is needed for the tip prediction, so let's try to explain the total_bill price instead.

The app and database has been uploaded to Heroku. Try it out here

## Outline
- [TL;DR](#TL;DR)
- [Background](#background)
- [Site Overview](#site-overview)
- [Comment on training](#comment-on-training)
- [Comment on database](#comment-on-database)
- [Comment on pytest](#comment-on-pytest)
- [Comment on deploying](#comment-on-deploying)
- [Run](#run)

## TL;DR
Prediction demo

## Background
The tips data set is a very basic example of regression. It still offers an opportunity to demonstrate many different aspects of machine learning for modeling, pipeline and serving. 

The EDA and modeling can be found in the notebook. The dataset is set up as two object, one to load the data and one to set up a pipeline with data transformation. For the models I mainly explore linear ones, after optimizing some non-linear models are tried, without improving metrics. And so I keep the simplest one for production.

The prediction service is set up like a microservice with two nodes. One with the prediction function and a db to save new data. 

The prediction model is set up for production using FastAPI and Docker. The code can be run by cloning the repo and running the docker or trying it out on Heroku. The prediction demo samples rows from the training dataset, predicts and returns the true value and the prediction as json data.

## Folder Layout
The folder layout is structured for the FastAPI prediction app, with support files for running on heroku in the root. However, since this is a demo Jupyter notebooks are uploaded as well as unit testing files.

XXX ADD FOLDER TREE



## Site Overview
The prediction and the data storage is separated, to be a bit more realistic. The repo db_data_service contains an sqlite database with the tips dataset. The dataset is divided in two tables, train and test. The data is accessed via http and served in json format.  



The various functionality can be accessed through the address field of the browser. For local implementation the address for the prediction function will be `'127.0.0.1:8000/predict/` and the Heroku address xxx. For the database it will be `127.0.0.1:8001/tips` and the Heroku address xxx. The following links are implemented
### Predict
* `/` returns hello world message and endpoints, with a desription, for this site.
* `/get_test_data` gets all the test data from the database and returns as json.
* `/get_random_test_data` gets a random row of test data from the database and returns as json data.
* '/get_test_prediction' gets a random row of test data from the database. Performs prediction. Saves test data and prediction to the prediction database. Returns prediction and the true value as json data

### Database
* `/` returns hello world message
* `/test_data` returns test data
* `/train_data` returns training data
* `/get_random_test_data` returns one random row of test data

## Coding Components
### Folder layout
### Notebooks - EDA and Training
### Serving - Heroku and FastAPI


## Site Overview


## Comment on Training
xxx
After some initial examination of the dataset the loading function, setting up of data subsets and creating the pipeline are done by two objects. The code is available in the notebooks folder as tipsdata.py and tipspipe.py.

## Comment on db
To demonstrate the prediction algorithm I just feed in a random row from the test dataset. So the database is set up to have two tables one with the training set and one with the test set. The database has some protection against injection through parameterized select statements.

There is also a database on the prediction site, to save the "new" query and the prediction, for future use and to make the demo slightly more realistic.

## Comment on pytest


## Comment on Deploying, FastAPI

## Run
### Heroku Site
* Click link

### Run from File
* Clone the db_service repo
* Run database. In the terminal, got to the database folder. Run `uvicorn api.router:app --reload --port 8001`
* Open browser at `127.0.0.1:8001/tips/`. The response will be "message: hello world tips" to confirm that it works.
* Clone pred_service repo
* Open the data_util file in the api folder. Change the clients to the host.docker ones
* In a terminal go to folder and run `uvicorn api.router:app --reload`
* Open a browser window at `127.0.0.1:8000/predict/`. The response will be "meassage: Hello world" to confirm that it works.

### Run from Docker
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
