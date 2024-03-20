from flask import Flask

import numpy as np
from scipy.stats import norm

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def calc_LV(mu, sigma, delta, epsilon, alpha):
    """
    Calculate the lending value.

    Parameters:
    mu (float): Expected return.
    sigma (float): Volatility of the asset, calculated as the standard deviation of historical asset returns.
    delta (float): The response period given to the client to adjust their position after a margin call.
    epsilon (float): The risk tolerance level, representing the maximum probability of the collateral value falling below the client exposure.
    alpha (float): The threshold level for the margin call.

    Returns:
    float: The calculated lending value.
    """

    # calculate the inverse CDF of the standard normal distribution for epsilon
    z_epsilon = norm.ppf(epsilon)

    # calculate LV
    num = (1 - alpha) * np.exp((mu - sigma**2 / 2) * delta + sigma * np.sqrt(delta) * z_epsilon)
    denom = 1 - alpha * np.exp((mu - sigma**2 / 2) * delta + sigma * np.sqrt(delta) * z_epsilon)
    lv = num / denom

    return lv

def calc_liq_LV(mu, sigma, delta, epsilon, alpha, x, gamma):
    """
    Calculate the liquidity-adjusted lending value.

    Parameters:
    mu (float): Expected return.
    sigma (float): Volatility of the asset, calculated as the standard deviation of historical asset returns.
    delta (float): The response period given to the client to adjust their position after a margin call.
    epsilon (float): The risk tolerance level, representing the maximum probability of the collateral value falling below the client exposure.
    alpha (float): The threshold level for the margin call.
    x (float): The transaction size.
    gamma (float): The liquidity parameter.

    Returns:
    float: The liquidity-adjusted lending value.
    """
    
    # calculate the inverse CDF of the standard normal distribution for epsilon
    z_epsilon = norm.ppf(epsilon)

    # calculate the liquidity-adjusted LV
    num = (1 - alpha) * np.exp(-gamma * x + (mu - sigma**2 / 2) * delta + sigma * np.sqrt(delta) * z_epsilon)
    denom = 1 - alpha * np.exp(-gamma * x + (mu - sigma**2 / 2) * delta + sigma * np.sqrt(delta) * z_epsilon)
    liq_lv = num / denom

    return liq_lv