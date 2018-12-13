from flask import Flask, render_template
from stockp.computer import GLOBAL


app = Flask(__name__)

@app.route('/')
def chart():
    limit, stocks, forecasts = tuple(GLOBAL)
    return render_template('chart.html', limit=limit, stocks=stocks, forecasts=forecasts)


if __name__ == '__main__':
    app.run()
