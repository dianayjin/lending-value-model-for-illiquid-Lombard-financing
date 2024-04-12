LV Model for Illiquid Lombard Financing
==============================
How does liquidity affect lending value in Lombard loans?

## Objective
The goal of this model is to understand the credit risk inherent in loans collateralized by liquid assets (e.g. stocks, bonds, funds) and to investigate the liquidity (size) effects on the riskiness of the transaction. Potential real world implementation of the model is illustrated in a Flask [`app.py`](<src\app\app.py>) and detailed methodology and results are documented in Jupyter [`notebooks`](<notebooks>). Please refer to the project organization tree below for more information.

## Setup Instructions
### Setting Up Your Development Environment
To run this project efficiently, you should set up a dedicated development environment. This ensures that the project dependencies do not conflict with those of other Python projects you might be working on. If you are already familiar with environments and/or use conda/mamba package managers, please skip to step 3.

1. **Create a virtual environment**: A virtual environment is a self-contained directory that contains a Python installation for a particular version of Python, plus a number of additional packages. This keeps your project isolated from the global Python environment. To create a virtual environment, navigate to the project's root directory and run the following command:
    - For macOS/Linux: `python3 -m venv venv`
    - For Windows: `py -m venv venv`

2. **Activate the virtual environment**: Before you install any packages, you need to activate your virtual environment. 
    - For macOS/Linux: `source venv\bin\activate`
    - For Windows: `.\venv\Scripts\activate`

    You should see the name of your virtual environment in parentheses at the beginning of your command-line prompt, indicating that the virtual environment is active.

3. **Install the required packages**: Once your virtual environment is active, you can install the required packages by running: `pip install -r requirements.txt`

    This command reads the `requirements.txt` file in your project directory and installs all of the packages listed there.

### Running the Flask Application

This project contains a Flask application in `src\app\app.py`. To run this application:

1. **Navigate to the app directory**: Change your directory to the `src\app` folder where `app.py` is located: `cd src\app`

2. **Set environment variables for Flask**: Before running the application, you need to set the environment variables used by Flask. 
    - For macOS/Linux: <br>
    `export FLASK_APP=app.py`<br>`export FLASK_ENV=development`
    - For Windows (cmd): <br>`set FLASK_APP=app.py`<br>`set FLASK_ENV=development`
    - For Windows (PowerShell): <br>`$env:FLASK_APP = "app.py"`<br> `$env:FLASK_ENV = "development"`

    Setting `FLASK_ENV` to `development` will enable debug mode, providing you with an interactive debugger and automatic reloader during development.

3. **Run the Flask app**: Start the application by running: `flask run`

    This will start a local web server. You can access the application by going to `http://127.0.0.1:5000/` in your web browser.

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized model summaries.
    │
    ├── notebooks          <- Jupyter notebooks. Contains project workflow and detailed methodology.
    │   └── html           <- Notebooks in HTML format.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment.
    │    
    └── src                <- Source code for use in this project. Code used to predict and train models can be found in notebooks.
        ├── __init__.py
        ├── app
        │    ├── app.py    <- Main app code.
        │    ├── examples  <- Example files used for presentation and app testing.
        │    ├── static    <- Static resources used in app.
        │    └── templates <- HTML files used in app.
        │
        ├── models         <- Scripts to run models used in app.
        │   └── lending_value.py
        │   
        └── visualization  <- Scripts to create graphics used in app. Also contains back-end code.
            └── visualize.py

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
