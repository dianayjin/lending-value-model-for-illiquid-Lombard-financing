import sys
import pandas as pd
import path
 
# directory reach
directory = path.Path(__file__).abspath()
 
# setting path
sys.path.append(directory.parent.parent)

import models.lending_value as lev
import visualization.visualize as vs

from flask import Flask, request, render_template

app = Flask(__name__)

# landing page
@app.route('/')

def index():
    return render_template('index.html')

# portfolio-builder page
@app.route('/portfolio-builder', methods=['GET', 'POST'])
def portfolio_builder():
    return vs.calc_ptf()

# multi-asset calculator page
@app.route('/multi-asset', methods=['GET', "POST"])
def multi_asset():
    return vs.calc_multi()

# single-asset calculator page
@app.route('/single-asset', methods=['GET', "POST"])
def single_asset():
    return vs.calc_single()

if __name__ == '__main__':
    app.run(debug=True)