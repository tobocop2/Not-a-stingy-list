import flask
import time

from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
from nasl_test import search_all_cities,get_results

app = flask.Flask(__name__)

@app.route('/')
def index():
    search_all_cities()
    get_results()
    env = Environment(loader=FileSystemLoader('templates'))
    tmpl = env.get_template('index.html')
    return flask.Response(tmpl.generate(result=get_results()))

app.run(debug=True,port=6666)
