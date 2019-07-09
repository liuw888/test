import os
import sys
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash
import datetime
from bs4 import BeautifulSoup

ALLOWED_EXTENSIONS = {'pdf', 'HTML', 'html'}

def allowed_file(filename):
    # check if the file is a html or pdf file
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)


def process_file(path, filename):
    page = open(path).read()
    soup = BeautifulSoup(page, 'lxml')
    rows = soup.find_all('tr')
    row_td = rows[0].find_all('td')
    header=['']*len(row_td)
    for x in range( len(row_td)-1):
        header[x] = BeautifulSoup(str(row_td[x]), "lxml").get_text()
    return render_template('index2.html',header=header,row_td=row_td)



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
