import plotly.graph_objs as go
from plotly.offline import plot

from plotly.subplots import make_subplots
import path
import sys
import numpy as np
 
# directory reach
directory = path.Path(__file__).abspath()
 
# setting path
sys.path.append(directory.parent.parent)

import models.lending_value as lev

import plotly.graph_objs as go
from plotly.offline import plot

from plotly.subplots import make_subplots
import path
import sys
import numpy as np
 
# directory reach
directory = path.Path(__file__).abspath()
 
# setting path
sys.path.append(directory.parent.parent)

import models.lending_value as lev

def make_plot(sigma, delta, epsilon, alpha, size, adtv, price):
    x_values = np.append(np.logspace(0, round(len(str(adtv))*1.5, None), 100, base=10), [[size]])
    lv_values = []
    loan_amount_values = []
    mu = (sigma ** 2) / 2
    gamma = 10 ** -1.87096 * adtv ** -0.794554

    for x in x_values:
        if x == size:
            size_lv = round(lev.calc_lv(mu, sigma, delta, epsilon, alpha, size, gamma), 2)
            size_loan_amount = round(size_lv * size * price, 2)
        else:
            lv = lev.calc_lv(mu, sigma, delta, epsilon, alpha, x, gamma)
            lv_values.append(lv)
            loan_amount = lv * x * price
            loan_amount_values.append(loan_amount)

    tickvals = [10**i for i in range(0, round(len(str(adtv))*1.5, None), 2)]

    # create subplots
    fig = make_subplots(rows=2, cols=1)

    # add trace
    fig.add_trace(
        go.Scatter(x=x_values, y=lv_values, mode='lines', name='LV', marker=dict(color='#015687'),
                   hovertemplate='# of stocks: %{x:.2e}<br>LV: %{y:.2%}<extra></extra>'),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=[size], y=[size_lv], mode='markers', name='Input', marker=dict(color='red'),
                   hovertemplate='# of stocks: %{x:.2e}<br>LV: %{y:.2%}<extra></extra>'),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=x_values, y=loan_amount_values, mode='lines', name='Loan Amount', marker=dict(color='#00C1FF'),
                   hovertemplate='# of stocks: %{x:.2e}<br>Loan Amount: %{y:,.2f} CHF<extra></extra>'),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=[size], y=[size_loan_amount], mode='markers', name='Input', marker=dict(color='red'),
                    hovertemplate='# of stocks: %{x:.2e}<br>Loan Amount: %{y:,.2f} CHF<extra></extra>'),
        row=2, col=1
    )

    # layout
    fig.update_layout(
        xaxis=dict(
            type='log',
            tickvals=tickvals
        ),
        xaxis2=dict(
            type='log',
            tickvals=tickvals,
            title='No. of Stocks'
        ),
        yaxis=dict(
            title='Liquidity-adjusted LV',
            tickvals=np.arange(0, 1.2, 0.2)
        ),
        yaxis2=dict(
            title='Loan Amount (CHF)'
        ),
        showlegend=False
    )

    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    return plot_div
