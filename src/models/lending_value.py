import numpy as np
from scipy.stats import norm

def calc_lv(mu, sigma, delta, epsilon, alpha, x, gamma):
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
    
    # calc the inverse CDF of the standard normal distribution for epsilon
    z_epsilon = norm.ppf(epsilon)

    # calc the liquidity-adjusted LV
    num = (1 - alpha) * np.exp(-gamma * x + (mu - sigma**2 / 2) * delta + sigma * np.sqrt(delta) * z_epsilon)
    denom = 1 - alpha * np.exp(-gamma * x + (mu - sigma**2 / 2) * delta + sigma * np.sqrt(delta) * z_epsilon)
    liq_lv = num / denom

    return liq_lv