import os, sys
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import bs4
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
