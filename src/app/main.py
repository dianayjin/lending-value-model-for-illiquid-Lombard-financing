import path
import sys
 
# directory reach
directory = path.Path(__file__).abspath()
 
# setting path
sys.path.append(directory.parent.parent)

import models.lending_value as lev
import visualization.visualize as vs

from flask import Flask, request, render_template_string, url_for

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])

def calculate():
    # default values and initialization
    plot_div = ""
    default_sigma = 0.15
    default_delta = 10 / 250
    default_epsilon = 0.01
    default_alpha = 0.25
    default_price = 0.00
    sigma, delta, epsilon, alpha, x, adtv, price = default_sigma, default_delta, default_epsilon, default_alpha, 0, 1, default_price
    mu, gamma, lv, liq_lv, loan_amount, error_message = 0, 0, 0, 0, 0, ''
 
    if request.method == "POST":
        try:
            sigma = float(request.form.get("sigma", default_sigma))
            x = int(request.form.get("x", 0))
            adtv = int(request.form.get("ADTV", 1))
            price = float(request.form.get("price", default_price))

            if sigma < 0 or sigma > 1 or x < 0 or adtv < 0 or price < 0:
                raise ValueError("Sigma must be between 0 and 1. X, ADTV, and stock price must be non-negative.")
            elif x == 0:
                raise ValueError("Setting transaction size to zero will calculate non-liquidity adjusted LV.")
            elif adtv == 0:
                raise ValueError('ADTV cannot be zero.')

            mu = (sigma ** 2) / 2
            delta = float(request.form.get("delta", default_delta))
            epsilon = float(request.form.get("epsilon", default_epsilon))
            alpha = float(request.form.get("alpha", default_alpha))

            if not 0 <= delta <= 1 or not 0 <= epsilon <= 1 or not 0 <= alpha <= 1:
                raise ValueError("Epsilon, Alpha, and Delta must be between 0 and 1.")

            gamma = 10 ** -1.87096 * adtv ** -0.794554

            lv = round(lev.calc_lv(mu, sigma, delta, epsilon, alpha, 0, gamma) * 100, 2)
            liq_lv = round(lev.calc_lv(mu, sigma, delta, epsilon, alpha, x, gamma) * 100, 2)
            loan_amount = format(x * liq_lv * price,',.2f')
            plot_div = vs.make_plot(sigma, delta, epsilon, alpha, x, adtv, price)
            
        except ValueError as e:     
            error_message = f'<b style="color: red;">WARNING:</b> {e}' 
    
    return render_template_string('''
        <html>
        <head>
            <title>LV Calculator</title>
            <link rel="icon" href="{{ url_for('static', filename='favicon.png') }}" type="image/png">
            <style>
                body { font-family: Arial, sans-serif; background-color: #f4f4f4; }
                .flex-container {
                    display: flex;
                    justify-content: center;
                    padding: 20px;
                }
                .main-container { 
                    width: 35%;
                    position: relative;
                    padding: 15px; 
                    background: white; 
                    border-radius: 8px; 
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); 
                    margin-right: 20px;
                }
                .reset-button-container {
                    position: absolute;
                    top: 10px;
                    right: 15px;
                }
                .plot-container {
                    flex-grow: 1;
                    padding: 15px;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                .header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    background: white;
                    padding-top: 15px;
                    padding-bottom: 15px;
                    padding-left: 20px;
                    padding-right: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    margin: auto;
                    width: 95%;
                }
                .logo {
                    width: 225px;
                    height: 50px;
                }
                input[type=number], input[type=submit] {
                    width: 100%;
                    padding: 8px;
                    margin: 4px 0;
                    border-radius: 4px;
                    border: 1px solid #ddd;
                }
                input[type=submit] {
                    background-color: #015687;
                    color: white;
                    border: none;
                    cursor: pointer;
                    font-weight: bold;
                }
                input[type=submit]:hover {
                    background-color: #002d47;
                }
            </style>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <script>
            function resetToDefault() {
                document.getElementById('sigma').value = '{{ default_sigma }}';
                document.getElementById('delta').value = '{{ default_delta }}';
                document.getElementById('epsilon').value = '{{ default_epsilon }}';
                document.getElementById('alpha').value = '{{ default_alpha }}';
                document.getElementById('x').value = '';
                document.getElementById('ADTV').value = '';
                document.getElementById('price').value = '{{ default_price }}';
                document.getElementById('error_message').innerHTML = '';
            }
        </script>
        <body>
            <div class="header">
                <h2 style="margin: 0; color:#002D47;">Lending Value Calculator for Lombard Loans</h2>
                <a href="http://127.0.0.1:5000">
                    <img src="{{ url_for('static', filename='svb_logo.png') }}" alt="SVB Logo" class="logo" style="width: 225px; height: 50px;">
                </a>                
            </div>
            <div class="flex-container">
                <div class="main-container">
                    <div class="reset-button-container">
                        <button type="button" onclick="resetToDefault()">Reset to Default</button>
                    </div>
                <form method="post">
                    Sigma: <input type="number" id="sigma" name="sigma" step="0.01" min="0" max="1" value="{{ request.form.sigma or default_sigma }}" required/><br />
                    Delta: <input type="number" id="delta" name="delta" step="0.01" min="0" max="1" value="{{ request.form.delta or default_delta }}" required/><br />
                    Epsilon: <input type="number" id="epsilon" name="epsilon" step="0.01" min="0" max="1" value="{{ request.form.epsilon or default_epsilon }}" required/><br />
                    Alpha: <input type="number" id="alpha" name="alpha" step="0.01" min="0" max="1" value="{{ request.form.alpha or default_alpha }}" required/><br />
                    Transaction Size (X): <input type="number" id="x" name="x" value="{{ request.form.x or 0 }}" min="0" required/><br />
                    ADTV: <input type="number" id="ADTV" name="ADTV" value="{{ request.form.ADTV or 1 }}" min="1" required/><br />
                    Stock Price (in CHF): <input type="number" id="price" name="price" value="{{ request.form.price or default_price }}" min="0.00" step="0.01" required/><br />
                    <input type="submit" value="Calculate" />
                </form>
                <p>{{ error_message|safe }}</p>
                <p><b>Calculated Mu</b>: {{ mu }}</p>
                <p><b>Calculated Gamma</b>: {{ gamma }}</p>
                <p><b>LV</b>: {{ lv }}%</p>
                <p><b>Liquidity-adjusted LV</b>: {{ liq_lv }}%</p>
                <p><b>Loan Amount (CHF)</b>: {{ loan_amount }}</p>
            </div>    
        <div class="plot-container">
            {{ plot_div|safe }}</div>
        </div>
        </body>
        </html>
        ''', plot_div=plot_div,
        error_message=error_message, mu=mu, gamma=gamma, lv=lv, liq_lv=liq_lv, loan_amount=loan_amount,
        sigma=sigma, delta=delta, epsilon=epsilon, alpha=alpha, x=x, adtv=adtv, price=price,
        default_sigma=default_sigma, default_delta=default_delta, 
        default_epsilon=default_epsilon, default_alpha=default_alpha, default_price=default_price)

if __name__ == "__main__":
    app.run(debug=True)