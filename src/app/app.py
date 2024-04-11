import sys
import path
import os
 
# directory reach
directory = path.Path(__file__).abspath()
 
# setting path
sys.path.append(directory.parent.parent)

import visualization.visualize as vs

from flask import Flask, render_template
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
    return vs.multi_asset()

# single-asset calculator page
@app.route('/single-asset', methods=['GET', "POST"])
def single_asset():
    return vs.single_asset()

if __name__ == '__main__':
    app.run(debug=True)