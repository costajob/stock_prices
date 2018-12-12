# Table of Contents
* [Scope](#scope)
* [Requirements](#requirements)
  * [Versions](#versions)
    * [Python 2](#python-2)
  * [Footprint](#footprint)
* [Design](#design)
  * [SRP](#srp)
  * [Data](#data)
  * [Tests](#tests)
* [Usage](#usage)
  * [Installation](#installation)
  * [Start Server](#start-server)
    * [Docker](#docker)
  * [APIs](#apis)
    * [Chart](#chart)
    * [Fresh](#fresh)
    * [JSON](#json)

# Scope
This is the implementation of the python code kata [Data Analysis and Visualisation](https://bitbucket.org/costajob/stock_prices/src/master/OBJECTIVES.md) for financial stock data.

# Requirements

## Versions
The library is compatible and it has been tested with the following python versions:

* 3.4.8

* 3.6.4

* 3.7.1 

### Python 2
Support for `old` python 2 is not guaranteed, since some components makes use of the `concurrent.futures` and `statistics` packages, introduced respectively since version `3.2` and `3.4`.  
It is possible to grant back-compatibility with version `2.7` by installing the external `futures` package, but it is pointless for the scope of this kata (considering support for version 2 will end on 2020).

## Footprint
To grant resiliency (and courtesy of the Python's broad standard library) the external dependencies footprint is kept to a minimum:

* [Flask](http://flask.pocoo.org/): a HTTP microframework, required by objectives (a plain WSGI server would have sufficed)

* [Gunicorn](https://gunicorn.org/): a pre-fork WSGI-compliant HTTP server, used to distribute the load among available cores

* [Meinheld](http://meinheld.org/): a WSGI-compliant Web server, based on green threads and asynchronous network I/O to reduce latency

* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/): an HTML parser library aimed at screen-scraping

# Design

## SRP
The code design follows the single responsibility principle by using a dedicated class for any specific task. Each class is confined within meaningful modules:

## Data
The stock closing data are fetched by remote HTML documents. The fetching is quite inefficient, since the whole document need to be downloaded and scanned in order to collect just last month prices, but the objectives do not advice using APIs, so it's implemented this way.

HTML documents are fetched once at server start and cached at `./stockp/data/corn.html` (etc.) to avoid further network latency. Just delete the cached HTML documents and restart `gunicorn` to fetch fresh copies.

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

## APIs
The library exposes the following HTTP endpoints at port `8888` (or at the port you bound at server start): 

### Chart
[0.0.0.0:8888/](http://0.0.0.0:8888/): returns a HTML chart representation of last month stock prices and their forecast for `Nasdaq`, `Corn` and `Gasoline` stocks.

### JSON
[0.0.0.0:8888/json](http://0.0.0.0:8888/json): returns a JSON data representation of last month stock prices and their forecast for `Corn`, `Gasoline` and `Nasdaq` stocks
tocks.
