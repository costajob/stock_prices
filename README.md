# Table of Contents
* [Scope](#scope)
* [Requirements](#requirements)
  * [Versions](#versions)
    * [Python 2](#python-2)
  * [Chart](#chart)
  * [Footprint](#footprint)
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

## Versions
The library is compatible and it has been tested with the following python versions:

* 3.4.8

* 3.6.4

* 3.7.1 

### Python 2
Support for `old` python 2 is not guaranteed, since some components makes use of the `concurrent.futures` introduced on standard library since version `3.2`.  

## Chart
The [chart.js](https://www.chartjs.org/) library is used in order to plot data into a non-static chart.  
The minimized script is loaded by an external `CDN`, thus requiring a network connection to properly works.

## Footprint
To grant resiliency (and courtesy of the Python's broad standard library) the external dependencies footprint is kept to a minimum:

* [Flask](http://flask.pocoo.org/): a WSGI-compliant HTTP micro-framework, required by objectives 

* [Gunicorn](https://gunicorn.org/): a pre-fork WSGI-compliant HTTP server, used to distribute the load among available cores

* [Meinheld](http://meinheld.org/): a WSGI-compliant Web server, based on green threads and asynchronous network I/O to reduce latency

* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/): a HTML parser library aimed at screen-scraping

# Design

## SRP
The code design follows the single responsibility principle by using a dedicated class for any specific task. Each class is confined within meaningful modules:

* `data`: data related objects, such as `Fetcher`, `Parser` and `Downloader`

* `entity`: plain value objects, such as `Stock`

* `computer`: core logic objects, such as `Forecaster`

## Data
The stock closing data are fetched by remote HTML documents. The fetching is quite inefficient, since the whole document need to be downloaded and scanned in order to collect just last month prices, but the objectives do not advise of any available APIs.  
HTML documents are fetched once at server start and cached at `./cache/corn.html` (etc.) to avoid further network latency. Just delete the cached HTML documents and restart `gunicorn` to fetch fresh copies.

## Tests
The library is covered, by fast, isolated unit and doc testing (the latter to grant reliable documentation):
```shell
python -m unittest discover -s stockp -p '*'
..........
----------------------------------------------------------------------
Ran 10 tests in 0.166s

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
python main.py
```

### Production
To start the server on production use the `gunicorn` executable by spawning as many workers as you need and by specifying the HTTP port:
```shell
gunicorn -w 4 -k meinheld.gmeinheld.MeinheldWorker -b :8888 main:app
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
The library exposes a single [HTTP endpoint](http://127.0.0.1:8888/) at port `8888` (or at the port you bound at server start), which renders a HTML chart representation of last month stock prices and their forecast for `Nasdaq`, `Corn` and `Gasoline` stocks:
