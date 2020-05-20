from flask import Flask
from flask_bootstrap import Bootstrap
import psycopg2, psycopg2.extras # move this to models.py
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = 'dev'
app.config['BOOTSTRAP_BTN_STYLE'] = 'secondary'


import routes






