from json import dumps
from flask import Flask, render_template
from stockp import computer, data


stocks = []
for tree in data.Downloader():
    parser = data.Parser(tree)
    stocks.append(list(parser))

forecasts = []
for entities in stocks:
    forecaster = computer.Forecaster(entities)
    forecasts.append(forecaster())

prices = (dumps([float(e) for e in entities]) for entities in stocks)

STOCKS = zip(('green', 'red', 'blue'), prices)
FORECASTS = zip(('corn', 'gasoline', 'nasdaq'), forecasts)

app = Flask(__name__)

@app.route('/')
def chart():
    return render_template('chart.html', limit=data.Parser.LIMIT, stocks=STOCKS, forecasts=FORECASTS)


if __name__ == '__main__':
    app.run()
