import os, sys
from flask import Flask
from bs4 import BeautifulSoup
import datetime




app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/hi")
def hi():
    return "Hi World!"

if __name__ == "__main__":
    app.run(debug=True)
