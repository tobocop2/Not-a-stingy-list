import time
from flask import Flask, request
from flask import Flask, jsonify, render_template, request, Response

from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
from nasl import threaded_search,search_all_cities,get_results

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        query = request.form['submit'].replace(' ','+')
        print 'printin query: '+query
        #query = '9c1'
        search_all_cities(query)
        result = threaded_search()
        #env = Environment(loader=FileSystemLoader('templates'))
        #tmpl = env.get_template('index.html')
        #return Response(tmpl.generate(result=get_results()))
        return render_template("index.html",result=result)
    else:
        return render_template("index.html",result = {})


app.run(debug=True,port=6666)
