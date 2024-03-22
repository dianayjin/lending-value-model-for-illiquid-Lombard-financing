import path
import sys
 
# directory reach
directory = path.Path(__file__).abspath()
 
# setting path
sys.path.append(directory.parent.parent)

import models.lending_value as lev
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])

def calculate():
    # Default values
    default_delta = 10 / 250
    default_epsilon = 0.01
    default_alpha = 0.25
    default_gamma = 4e-10  # Example small value

    if request.method == "POST":
        try:
            sigma = float(request.form.get("sigma", 0))
            x = float(request.form.get("x", 0))
            gamma = float(request.form.get("gamma", default_gamma))

            if sigma < 0 or sigma > 1 or x < 0 or gamma < 0:
                raise ValueError("Sigma must be between 0 and 1. Other values must be non-negative.")

            mu = (sigma ** 2) / 2  # Calculated as mu = (sigma^2) / 2
            delta = float(request.form.get("delta", default_delta))
            epsilon = float(request.form.get("epsilon", default_epsilon))
            alpha = float(request.form.get("alpha", default_alpha))

            # Calculate LV and Liquidity-adjusted LV
            lv = lev.calc_LV(mu, sigma, delta, epsilon, alpha)
            liq_lv = lev.calc_liq_LV(mu, sigma, delta, epsilon, alpha, x, gamma)

            return render_template_string('''<form method="post">
                Sigma: <input type="number" name="sigma" step="any" min="0" max="1" required/><br />
                Delta: <input type="number" name="delta" step="any" min="0" value="{{ default_delta }}"/><br />
                Epsilon: <input type="number" name="epsilon" step="any" min="0" value="{{ default_epsilon }}"/><br />
                Alpha: <input type="number" name="alpha" step="any" min="0" value="{{ default_alpha }}"/><br />
                Transaction Size (X): <input type="number" name="x" step="any" min="0" required/><br />
                Gamma: <input type="number" name="gamma" step="any" min="0" placeholder="e.g., 4e-10" value="{{ default_gamma }}"/><br />
                <input type="submit" value="Calculate" />
                </form>
                <p>Calculated Mu: {{ mu }}</p>
                <p>LV: {{ lv }}</p>
                <p>Liquidity-adjusted LV: {{ liq_lv }}</p>
                ''', lv=lv, liq_lv=liq_lv, mu=mu, default_delta=default_delta, default_epsilon=default_epsilon, default_alpha=default_alpha, default_gamma=default_gamma)
        except ValueError as e:
            return render_template_string('''<p>Error: {{ error_message }}</p>''' + '''[your form HTML here]''', error_message=str(e))

    # Display form with default values
    return render_template_string('''<form method="post">
        Sigma: <input type="number" name="sigma" step="any" min="0" max="1" required/><br />
        Delta: <input type="number" name="delta" step="any" min="0" value="{{ default_delta }}"/><br />
        Epsilon: <input type="number" name="epsilon" step="any" min="0" value="{{ default_epsilon }}"/><br />
        Alpha: <input type="number" name="alpha" step="any" min="0" value="{{ default_alpha }}"/><br />
        Transaction Size (X): <input type="number" name="x" step="any" min="0" required/><br />
        Gamma: <input type="number" name="gamma" step="any" min="0" placeholder="e.g., 4e-10" value="{{ default_gamma }}"/><br />
        <input type="submit" value="Calculate" />
        </form>''', default_delta=default_delta, default_epsilon=default_epsilon, default_alpha=default_alpha, default_gamma=default_gamma)

if __name__ == "__main__":
    app.run(debug=True)