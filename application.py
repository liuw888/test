import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import sys
from bs4 import BeautifulSoup
import lxml.html as lh
import datetime
from graphviz import Digraph



app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/hi")
def hi():
    return "Hi World!"

if __name__ == "__main__":
    app.run(debug=True)
