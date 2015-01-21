#from flask import Flask, jsonify, render_template, request
#from jinja2 import Environment
#from jinja2.loaders import FileSystemLoader
#from user_agents import user_agents
import nasl

#app = Flask(__name__)

#@app.route('/')
def print_results():
    #query = request.args.get['a'].replace(' ','+')
    query = '9c1'
    #query = request.form['submit'].replace(' ','+')
    results = nasl.get_results(nasl.search_all_cities(query))
    for result in results:
        print str(result)+'\n'+str(results[result])
    #return jsonify(result=get_results())
    #return render_template("index.html", results=results)


#if __name__ == "__main__":
    #app.run(debug=True)
print_results()
