import os
import sys
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash
import datetime
from bs4 import BeautifulSoup
from graphviz import Digraph
import pybase64


@app.route('/', methods=['GET', 'POST'])
def index():
    print('app works')
  
    chart_data = Digraph()
    chart_data.node('H', 'Hello')
    chart_data.node('W', 'World')
    chart_data.edge('H', 'W')
    chart_output = chart_data.pipe(format='png')
    chart_output = pybase64.b64encode(chart_output).decode('utf-8')
    return render_template('index.html',chart_output=chart_output)


@app.route("/hi")
def hi():
    return "Hi World!"



if __name__ == "__main__":
    app.run(debug=True)
