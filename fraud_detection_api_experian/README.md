# Task: Fraud detection api
A web application that has post endpoint called *fraud_detection* which takes credit data to predict the probability of fraud. 

There is training script included for how to train a model in production for this. 
 
# Tech used:
- python
- FastAPI
- docker
- pytest
- xgbooost


# Instructions for running the code
 - Please make sure you have docker installed on your machine.

## Run fraud detection api using docker:
1. Build docker image for fraud_detection_api:

```
docker compose build fraud_detection_api
```

2. Run docker image for google_eyes_api:

```
docker compose up fraud_detection_api
```

3. Web application is running at ```http://localhost:8000```

4. Run heathcheck endpoint using:
```
curl --location --request GET 'http://0.0.0.0:8000/ping'
```

5. Run fraud detection post method endpoint using:
```
curl --location 'http://0.0.0.0:8000/fraud_detection' \
--header 'Content-Type: application/json' \
--data '[{
    "customer_id": 345435,
    "number_of_open_accounts": 23,
    "total_credit_limit": 12345,
    "total_balance": 200000,
    "number_of_accounts_in_arrears": 2
}]'
```
Update the image name to test in on different images.

6. Application testing in postman: I have uploaded the postman collection.
    - Import the collection in postman
    - Run fraud_detection endpoint:
    - Go to Body -> select raw -> select JSON
    - Pass the input to request like 
    
    *[{
        "customer_id": 345435,
        "number_of_open_accounts": 23,
        "total_credit_limit": 12345,
        "total_balance": 200000,
        "number_of_accounts_in_arrears": 2
    }]*

   - Output should be a list of fraud probabilities
    ![output_example](./output%20examples/example_output.png)

## Run tests using docker:
```
docker compose build tests
docker compose run tests
```

## Linting the whole project:
```
docker compose build lint
docker compose run lint
```

## Experimentation in jupyter:
```
docker compose up jupyter
```
Jupyter notebooks will be available at localhost port `9000`



### Things I worked on:
### Rest API:
1. Used FastAPI to serve ML requests.
2. I have used poetry for dependency management and packaging.
3. I have created different folders inside /src to apply seperation of conecerns. So the main business
logic is inside the /services folder, and /routes only deals with the incoming requests and redirects to particular service.
4. There is Schema defined for input and output of the /fraud_detection endpoint. 
5. Added type hint so that we know what is the type of the input and output for given functions.
6. App will throw validations errors on the incoming requests for /fraud_detection endpoint. 
7. Exception handling is added in the code.
8. Tests: Tests have been added to verify if system is working fine. I have used pytest for this.
9. Logging: Added more meaningful logs which will help us monitor/reverify if something goes wrong.
11. Docker: Used Docker to build the whole web application. Docker compose file contains multiple services on how to run main application, tests, linting, jupyter, etc.

### Model training:
1. I have added training script under src/fraud_detection_api/training folder.
2. train_xgboost.py file contains main class for training the model. 
3. model_fitter.py file contains code for how to call train_xgboost model
4. I could have added code for hyper param optimistaion as well. Didn't get time to work on it.



## Things I could have looked into -> 
1. Spend more time to experiment on different models to use for the fraud detection. Hyper param optimisation script. Also, I could have added mlflow for model experimentation or model tracking purpose.

2. Spend more time to test more corner cases with various different inputs

2. Promotheus: Use Promotheus for metrics collection like latency, error rates, http status codes, resource utilisation. It scrpaes the metrics from web app.

3. Grafana: Promotheus can be integrated with Grafana for visualization, alerting.
   
4. Write more test cases to increae the coverage. Maybe run test cases through the script.

5. Write CI pipeline to check the code, test the code, linting the code properly, code build and etc.

6. Scale the application using kubernetes which can handle in various levels of traffic and workload. You can easily scale the system and keep it at high availability all times.



# NOTE:
High level design of training and rest api web app. ![output_example](./output%20examples/training_serving_pipeline.png)


