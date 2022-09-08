## Tips Dataset
[Web demo] prediction(http://patricks-predictions.herokuapp.com/predict/) database [online access](http://db-data-service.herokuapp.com/tips/)
### TL;DR
The tips data set is a very basic example of regression. It still offers an opportunity to demonstrate many different aspects of machine learning for modeling, pipeline and serving. 

The EDA and modeling can be found in the notebook. The dataset is set up as two object, one to load the data and one to set up a pipeline with data transformation. For the models I mainly explore linear ones, after optimizing some non-linear models are tried, without improving metrics. And so I keep the simplest one for production.

The prediction service is set up like a microservice with two nodes. One with the prediction function and a db to save new data. 

The prediction model is set up for production using FastAPI and Docker. The code can be run by cloning the repo and running the docker or trying it out on Heroku. The prediction demo samples rows from the testing dataset, predicts and returns the true value and the prediction as json data.
Try prediction [here](http://patricks-predictions.herokuapp.com/predict/)(the web site is served on a free Heroku dyno, so you might have to call the first endpoint twice), access database [here](http://db-data-service.herokuapp.com/tips/), database code in github [here](https://github.com/CJRockball/db_data_service)

### 1. Dataset
The data is 243 rows of restaurant related information. I try to predict the total bill from a set of categorical (ordinal and nominal) and contiuous features. After an initial review I created two data related objects ([testdata](https://github.com/CJRockball/pred_service/blob/main/notebooks/tipsdata.py) and [testpipe](https://github.com/CJRockball/pred_service/blob/main/notebooks/tipspipe.py)). Tipsdata downloads and splits the dataset in train, val and test. Tipspipe creates sklearn pipeline for transformations and models. These are used as backends for the EDA/model [notebook](https://github.com/CJRockball/pred_service/blob/main/notebooks/eda_model.ipynb) 

### 2. EDA
The EDA starts with examening the dataset, there are no missing values. Then I count, rows, features, labels etc. Then there is a visual inspection of the balance of features, some of them are quite unbalanced. Unfortunately the dataset is too small to downsample. I use IQR charts to determine if the categorical features correlate to the label. Only group size has a strong correlation.  Then I look at the distribution of the continuous feature, tips, and the label, total_bill. Both are skewed and are log-transformed in the pipeline. Finally the correlation between them is calculated and visualized. There is a reasonably strong correlation. Based on this analysis we use the group_size, time and tips features. I normalize the the ordinal feature group_size and the continuous tips.

### 3. Model/Prdictions


### 4. Microservice
To demonstrate predictions I will get one row from the test data and run prediction so that it can be compared to the true answer. To make it a bit more realistic I save the data (train and test) on one server ([database server](https://github.com/CJRockball/db_data_service) and have the model on another. The database can be accessed via the web through FastAPI [here](), the endpoints are displayed at the root site. The prediction site can be accessed [here](), the endpoints are displayed here. 
When the prediction site is accessed it makes a call over http to retrieve data from the database. The prediction is made and returned as json data. Finally the data used for prediction (the "new" data) is saved in a database on the prediction server, for future retuning of the model.
![](https://github.com/CJRockball/pred_service/blob/main/static/prediction%20microservice.png)

### 5. Displaying with FastAPI
FatAPI is used to display the data (see main script [here](https://github.com/CJRockball/pred_service/blob/main/api/main.py)). It has type control and verification, however all of that is done on the database server. The prediction server endpoints have exception control so it doesn't crash of the database is down or the wrong information is returned. The server also has basic logging implemented.

### 6. Pytest
Pytest is used to unit test functions. This is usually not included in the repo, but kept in here for demo purpose.
![](https://github.com/CJRockball/pred_service/blob/main/static/coverage.png)

### 7. Serving with Docker and Heroku 
All the scripts are packaged with Docker. The whole app can be downloaded and run with docker, see the [run description](#Run-from-Docker). I have also uploaded the app to Heroku for online testing. 

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
