from flask import Flask, render_template    
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/hi")
def hi():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)