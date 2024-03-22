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
    # default values and init
    default_sigma = 0.15
    default_delta = 10 / 250
    default_epsilon = 0.01
    default_alpha = 0.25
    sigma, delta, epsilon, alpha, x, adtv = default_sigma, default_delta, default_epsilon, default_alpha, 0, 1
    mu, gamma, lv, liq_lv, error_message = 0, 0, 0, 0, ''
 
    if request.method == "POST":
        try:
            sigma = float(request.form.get("sigma", default_sigma))
            x = int(request.form.get("x", 0)) 
            adtv = int(request.form.get("ADTV", 1)) 

            if sigma < 0 or sigma > 1 or x < 0 or adtv < 0:
                raise ValueError("Sigma must be between 0 and 1. X and ADTV must be non-negative integers.")
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

            lv = lev.calc_lv(mu, sigma, delta, epsilon, alpha, 0, gamma)
            liq_lv = lev.calc_lv(mu, sigma, delta, epsilon, alpha, x, gamma)

        except ValueError as e:     
            error_message= f'<b style="color: red;">WARNING:</b> {e}' 
    
    return render_template_string('''
        <html>
        <head>
            <title>LV Calculator</title>
            <link rel="icon" href="{{ url_for('static', filename='favicon.png') }}" type="image/png">
            <style>
                body { font-family: Arial, sans-serif; background-color: #f4f4f4; }
                .container { 
                    width: 80%; 
                    margin: 20px auto; 
                    padding: 20px; 
                    background: white; 
                    border-radius: 8px; 
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); 
                    position: relative;
                }
                .reset-button-container {
                    position: absolute;
                    top: 10px;
                    right: 10px;
                }
                .header { display: flex; justify-content: space-between; align-items: center; }
                input[type=number], input[type=submit] {
                    width: 100%;
                    padding: 10px;
                    margin: 6px 0 20px;
                    border-radius: 4px;
                    border: 1px solid #ddd;
                }
                input[type=submit] {
                    background-color: #3294d1;
                    color: white;
                    border: none;
                    cursor: pointer;
                    font-weight: bold;
                }
                input[type=submit]:hover {
                    background-color: #226894;
                }
                .logo { width: 50px; height: 50px; }
            </style>
        </head>
        <script>
        function resetToDefault() {
            document.getElementById('sigma').value = '{{ default_sigma }}';
            document.getElementById('delta').value = '{{ default_delta }}';
            document.getElementById('epsilon').value = '{{ default_epsilon }}';
            document.getElementById('alpha').value = '{{ default_alpha }}';
            document.getElementById('x').value = '';
            document.getElementById('ADTV').value = '';
            document.getElementById('error_message').value = '';
        }
        </script>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Lending Value Calculator for Lombard Loans</h2>
                    <a href="http://127.0.0.1:5000">
                    <img src="{{ url_for('static', filename='svb_logo.png') }}" alt="SVB Logo" class="logo" style="width: 225px; height: 50px;">
                    </a>                
                </div>
            <div class="container">
                <div class="reset-button-container">
                    <button type="button" onclick="resetToDefault()">Reset to Default</button>
                </div>
                <form method="post">
                    Sigma: <input type="number" id="sigma" name="sigma" step="0.01" min="0" max="1" value="{{ sigma }}" required/><br />
                    Delta: <input type="number" id="delta" name="delta" step="0.01" min="0" max="1" value="{{ delta }}" required/><br />
                    Epsilon: <input type="number" id="epsilon" name="epsilon" step="0.01" min="0" max="1" value="{{ epsilon }}" required/><br />
                    Alpha: <input type="number" id="alpha" name="alpha" step="0.01" min="0" max="1" value="{{ alpha }}" required/><br />
                    Transaction Size (X): <input type="number" id="x" name="x" value="{{ x }}" min="0" required/><br />
                    ADTV: <input type="number" id="ADTV" name="ADTV" value="{{ adtv }}" min="1" required/><br />
                    <input type="submit" value="Calculate" />
                </form>
                <p>{{ error_message|safe }}</p>
                <p><b>Calculated Mu</b>: {{ mu }}</p>
                <p><b>Calculated Gamma</b>: {{ gamma }}</p>
                <p><b>LV</b>: {{ lv }}</p>
                <p><b>Liquidity-adjusted LV</b>: {{ liq_lv }}</p>
            </div>
        </body>
        </html>
        ''', error_message=error_message, mu=mu, gamma=gamma, lv=lv, liq_lv=liq_lv,
           sigma=sigma, delta=delta, epsilon=epsilon, alpha=alpha, x=x, adtv=adtv,
           default_sigma=default_sigma, default_delta=default_delta, 
           default_epsilon=default_epsilon, default_alpha=default_alpha)

if __name__ == "__main__":
    app.run(debug=True)