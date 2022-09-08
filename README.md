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
### 1. Dataset
The data is 243 rows of restaurant related information. I try to predict the total bill from a set of categorical (ordinal and nominal) and contiuous features. After an initial review I created two data related objects ([testdata](https://github.com/CJRockball/pred_service/blob/main/notebooks/tipsdata.py) and [testpipe](https://github.com/CJRockball/pred_service/blob/main/notebooks/tipspipe.py)). Tipsdata downloads and splits the dataset in train, val and test. Tipspipe creates sklearn pipeline for transformations and models. These are used as backends for the EDA/model [notebook](https://github.com/CJRockball/pred_service/blob/main/notebooks/eda_model.ipynb) 

### 2. EDA
The EDA starts with examening the dataset, there are no missing values. Then I count, rows, features, labels etc. Then there is a visual inspection of the balance of features, some of them are quite unbalanced. Unfortunately the dataset is too small to downsample. I use IQR charts to determine if the categorical features correlate to the label. Only group size has a strong correlation.  Then I look at the distribution of the continuous feature, tips, and the label, total_bill. Both are skewed and are log-transformed in the pipeline. Finally the correlation between them is calculated and visualized. There is a reasonably strong correlation. Based on this analysis we use the group_size, time and tips features. I normalize the the ordinal feature group_size and the continuous tips.

### 3. Model/Prdictions

### 4. Microservice
To demonstrate predictions I will get one row from the test data and run prediction so that it can be compared to the true answer. To make it a bit more realistic I save the data (train and test) on one server ([database server](https://github.com/CJRockball/db_data_service) and have the model on another. The database can be accessed via the web through FastAPI [here](), the endpoints are displayed at the root site. The prediction site can be accessed [here](), the endpoints are displayed here. 
When the prediction site is accessed it makes a call over http to retrieve data from the database. The prediction is made and returned as json data. Finally the data used for prediction (the "new" data) is saved in a database on the prediction server, for future retuning of the model.

### 5. Displaying with FastAPI
FatAPI is used to display the data (see main script [here](https://github.com/CJRockball/pred_service/blob/main/api/main.py)). It has type control and verification, however all of that is done on the database server. The prediction server endpoints have exception control so it doesn't crash of the database is down or the wrong information is returned. The server also has basic logging implemented.

### 6. Pytest
Pytest is used to unit test functions. This is usually not included in the repo, but kept in here for demo purpose.



### 7. Serving with Docker and Heroku 
All the scripts are package with Docker. The whole app can be run with docker, see the [run description](#Run-from-Docker). 

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
