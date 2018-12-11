# Data Analysis and Visualisation Description

## Objectives
This project aims to collect, visualise and forecast financial data with python.
In specific we want to download stock closing price for Corn, Gasoline and Nasdaq and plot them on a same chart where at least the 1 month of data is available.

For instance stock prices could be downloaded from:

* [Corn](https://finance.yahoo.com/quote/CORN/history?p=CORN)

* [Gasoline](https://finance.yahoo.com/quote/UGA/history?p=UGA)

* [Nasdaq](https://finance.yahoo.com/quote/NDAQ/history?p=NDAQ)

In addition to the chart, you should also add a table with the next day closing price forecast for each stock. The forecast could be computed as average of the previous 3 days.

## Project requirements
* Please note that the code should not be published on the web.
* Please complete this technical assignment within 7 days and send back to us a .zip folder with the code.
* The project should follow a test-driven-development (TDD) approach.
* The application must run on a Flask server and the chart should not be a static JPG or PNG image
* The Flask server must contain a naive front-end panel which displays chart and table
* Based on your skills please focus on the aspect you feel more confident, for instance: responsive webpage, well designed front-end, optimized code, unit tests, data structure, etc.
* Regarding the price forecast, if needed you could use scientific libraries (numpy, pandas, scikit-learn). Otherwise just apply a simple concepts i.e. average price of the previous 3 days.
* A good knowledge of Python should be proved within the code.
* Run the service inside a Docker container.

### Optional
* Stock prices could be collected via API
* You could back test your prediction on historical data and provide a confidence score
      
## Notes
* DO NOT INCLUDE into the `.zip` folder any executable file, e.g. file with `.exe`, `.lib` or `.msi` extension.
* A well-written code should explain itself, but comments within the code are encouraged :)
* Your code should be ready for a production environment.

## Validation
In order to run your code and tests please include in your zip a README file with additional instructions. Anyhow, we expect to execute your code as following:

### Python 2.7
```shell
pip install -t lib -r requirements.txt python main.py
```

### Python 3
```shell
pip3 install -t lib -r requirements.txt python3 main.py
```

### Example
Please use the following example as starting point to develop this project: 

#### 1. Save in a `main.py` file the following:
```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
```

#### 2. Save in a requirements.txt file the following:
```txt
Flask==0.12.2
```

#### 3. Finally run it as following:
```shell
pip install -t lib -r requirements.txt
python main.py
```
