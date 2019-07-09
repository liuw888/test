import os, sys
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import datetime




app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request', file=sys.stderr)
            return redirect(request.url)
        file = request.files['file']
        print(file, file=sys.stderr)
        if file.filename == '':
            print('No file selected', file=sys.stderr)
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            process_file(os.path.join(
                app.config['UPLOAD_FOLDER'], filename), filename)
            return redirect(url_for('uploaded_file', filename=filename))
    print('App works', file=sys.stderr)
    return render_template('index.html')

@app.route("/hi")
def hi():
    return "Hi World!"

if __name__ == "__main__":
    app.run(debug=True)
