from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("home.html")

@app.route("/hi")
def hi():
    return "Hi World!"

if __name__ == "__main__":
    app.run(debug=True)
