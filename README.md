# Table of Contents
* [Scope](#scope)
* [Design](#design)
  * [SRP](#srp)
  * [Data](#data)
  * [Tests](#tests)
* [Usage](#usage)
  * [Installation](#installation)
  * [Start Server](#start-server)
    * [Docker](#docker)
  * [API](#api)

# Scope
This is the implementation of the python code kata [Data Analysis and Visualisation](https://bitbucket.org/costajob/stock_prices/src/master/OBJECTIVES.md) for financial stock data.

# Requirements

## Version
The library is compatible and it has been tested with python versions:

* 2.7.15

* 3.4.8

* 3.7.1 

## Footprint
To grant resiliency (and courtesy of the Python's broad standard library) the external dependencies footprint is kept to a minimum, but for `gunicorn` and `meinheld` libraries, which are used to wrap the WSGI HTTP server in order to augment throughput.

# Design

## SRP
The code design follows the single responsibility principle by using a dedicated class for any specific task. Each class is confined within meaningful modules:

## Data
The stock closing data are fetched by a remote HTML documents. The documents are fetched once at server start and cached at `./stockp/data/corn.html` (etc.) to avoid further network latency. Just delete the cached HTML documents and restart `gunicorn` to fetch fresh copies.

## Tests
The library is covered, by fast, isolated unit and doc testing (the latter to grant reliable documentation):
```shell
python -m unittest discover -s stockp -p '*'
..................
----------------------------------------------------------------------
Ran 19 tests in 0.008s

OK
```

# Usage
Depending on your python version use the appropriate binaries available on your workstation:

## Installation
Install the external dependencies via `pip`:
```shell
pip install -r requirements.txt
```

## Start Server

### Development
To start the WSGI server on development just execute the `main.py` file with the python binary:
```shell
python ./main.py
```

### Production
To start the server on production use the `gunicorn` executable by spawning as many workers as you need and by specifying the HTTP port:
```shell
gunicorn -w 4 -k meinheld.gmeinheld.MeinheldWorker -b :8888 main:Stockp
```
### Docker
This application can be built and deployed as a [Docker](https://www.docker.com/) container by relying on the `python:3.7.1` official image:
```shell
docker build -t stockp .
```

Once the container has been built, just run it by:
```shell
docker run -d -p 8888:8888 stockp
```

## API
The library exposes the following HTTP endpoints at port `8888` (or at the port you bound at server start): 

* [0.0.0.0:8888/](http://0.0.0.0:8888/): returns a HTML chart representation of last month stock prices and their forecast for `Nasdaq`, `Corn` and `Gasoline` stocks

* [0.0.0.0:8888/fetch](http://0.0.0.0:8888/fetch): fetch a fresh copy of prices for `Corn`, `Gasoline` and `Nasdaq` stocks

* [0.0.0.0:8888/json](http://0.0.0.0:8888/json): returns a JSON data representation of last month stock prices and their forecast for `Corn`, `Gasoline` and `Nasdaq` stocks
tocks

