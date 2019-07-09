import os
import sys
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash
import datetime
from bs4 import BeautifulSoup
from graphviz import Digraph

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'
ALLOWED_EXTENSIONS = {'pdf', 'HTML', 'html'}


app = Flask(__name__, static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

def allowed_file(filename):
    # check if the file is a html or pdf file
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_file(path, filename):
    convertToPDF(path, filename)

def convertToPDF(path, filename):
    print("convert function works", file = sys.stderr)
    os.environ["PATH"] += os.pathsep + \
        'C:/Program Files (x86)/Graphviz2.38/bin/'

    dot = Digraph('structs', node_attr={'shape': 'plaintext'})
    dot
    check=False
    page = open(path).read()
    soup = BeautifulSoup(page, 'lxml')
    rows = soup.find_all('tr')
    print(rows,file = sys.stderr)
    print(len(rows), file = sys.stderr)

    i = 1
    edge = []
    j = 1
    row_td = rows[0].find_all('td')
    header=['']*len(row_td)
    print(len(row_td))
    for x in range( len(row_td)-1):
        header[x] = BeautifulSoup(str(row_td[x]), "lxml").get_text()
    print(header[:7])
    if(header[0]=="Phase" and header[1]=='Task' and header[2]=='Actual Agent'
        and header[3] =='Forwarded To' and header[4] =='Forwarded By' and header[5]=='Status'
        and header[6]=='Staff Chg' and header[7]=='Date'):
        check = True

    while(i < len(rows)-1):
        row_td = rows[i].find_all('td')
        # print(row_td)
        # print(type(row_td))

        str_cells = str(row_td[8])
        statusText = BeautifulSoup(str_cells, "lxml").get_text()
        status = str(statusText)

        if(status == "Completed- Successfully" or status == "Released- Notified" or status == "Released"
           or status == 'Released- Waiting' or status == "Completed- Aborted"
           or "Failure" in status):
            marker = ""
            color = ""
            order = 'sturct'+str(j)
            if(j > 1 and (status=="Released" or status=="Released- Waiting")):
                preorder = 'sturct'+str(preindex+1)
            elif(j > 1):
                preorder = 'sturct'+str(j-1)
                preindex = j-1

            time_cell = str(row_td[7])
            time = BeautifulSoup(time_cell, "lxml").get_text()
            if("." in time):
                dateDay = time[:10]
                dateArr = dateDay.split(".")
                dateDay = dateArr[2]+"/"+dateArr[1]+"/"+dateArr[0]
            elif("/" in time):
                dateDay = time[:10]
                dateArr = dateDay.split("/")
                dateDay = dateArr[2]+"/"+dateArr[0]+"/"+dateArr[1]
            else:
                dateDay = time[:4]+"/"+time[4:6]+"/"+time[6:8]

            d0 = datetime.date.today()
            d1 = datetime.date(int(dateDay[0:4]), int(dateDay[5:7]), int(dateDay[8:]))
            delta = d0 - d1
            daypass = str(delta.days)
            print(daypass)

            status_cell = str(row_td[8])
            statusText = BeautifulSoup(status_cell, "lxml").get_text()
            status = str(statusText)
            # print(status)

            if(status == 'Completed- Successfully'):
                marker = "Completed"
                bcolor = "#98FB98"
            elif(status == 'Released- Notified'):
                marker = "Pending %s days" % daypass
                bcolor = "#FFA500"
            elif(status == 'Released- Waiting' or status == 'Released'):
                marker = "Waiting"
                bcolor = "#FADA5E"
            elif(status == "Completed- Aborted"):
                marker = "Aborted"
                bcolor = "#C21807"
            elif (status == "Completed- Staffing Failure"):
                marker = "Staff failure"
                bcolor = "#C21807"

            task_cell = str(row_td[1])
            task = BeautifulSoup(task_cell, "lxml").get_text()
            task = task.replace("&", "and")
            print(task)

            people_name = str(row_td[2])
            people = BeautifulSoup(people_name, "lxml").get_text()
            peoplenames = people.split(',')
            print(peoplenames)
            peopleName = people
            k = 0
            if(len(peoplenames) > 3):
                peopleName = ""
                for x in range(len(peoplenames)):
                    k = k+1
                    peopleName = peopleName + peoplenames[x] + ", "
                    if(k % 3 == 0):
                        peopleName += "<br/>"

            if(marker == "Waiting"):
                dot.node(order, '''<
                <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="8">
                        <tr >
                            <td colspan ="4" bgcolor='%s'>Waiting</td>
                        </tr>
                        <tr>
                            <td rowspan ="3" colspan ="3" ><img  src="C:\waiting.png"></img></td>
                        </tr>
                        <tr>
                            <td>%s</td>
                        </tr>
                        <tr>
                            <td>%s</td>
                        </tr>
                </TABLE>>''' % (bcolor, task, peopleName))

            elif(marker == "Completed"):
                dot.attr('node', imagescale='height')

                dot.node(order, '''<
                <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
                        <tr >
                            <td colspan ="4" bgcolor='%s'>Completed</td>
                        </tr>
                        <tr>
                            <td rowspan ="4" colspan ="3" ><img  src="C:\ok.png" ></img></td>
                        </tr>
                        <tr>
                            <td> %s</td>
                        </tr>
                        <tr>
                            <td>%s</td>
                        </tr>
                        <tr>
                            <td>%s</td>
                        </tr>
                </TABLE>>''' % (bcolor, task, peopleName, dateDay))

            elif("Pending" in marker):
                dot.node(order, '''<
                <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="8">
                    <tr >
                        <td colspan ="4" bgcolor='%s'>%s</td>
                    </tr>
                    <tr>
                        <td rowspan ="4" colspan ="3" ><img  src="C:\working.png" ></img></td>
                    </tr>
                    <tr>
                        <td> %s</td>
                    </tr>
                    <tr>
                        <td>%s</td>
                    </tr>
                    <tr>
                        <td>Since %s</td>
                    </tr>
                </TABLE>>''' % (bcolor, marker, task, peopleName, dateDay))

            elif(marker == "Staff failure"):
                dot.node(order, '''<
                <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
                    <tr >
                        <td colspan ="4" bgcolor='%s'>%s</td>
                    </tr>
                    <tr>
                        <td rowspan ="5" colspan ="3" ><img  src="C:\staff.png" ></img></td>
                    </tr>
                    <tr>
                        <td> %s</td>
                    </tr>
                    <tr>
                        <td>%s</td>
                    </tr>
                    <tr>
                        <td>%s</td>
                    </tr>
                    <tr>
                        <td>For support: <u><font color="blue">http://manage-info.intranet.dow.com/Forms/DS/DS-MMD/F_DS_MMD-MSOR.asp</font></u></td>
                    </tr>
                </TABLE>>''' % (bcolor, marker, task, peopleName, dateDay))

            else:
                dot.node(order, '''<
                <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
                    <tr >
                        <td colspan ="4" bgcolor='%s'>%s</td>
                    </tr>
                    <tr>
                        <td rowspan ="4" colspan ="3" ><img  src="C:\wrong.png" ></img></td>
                    </tr>
                    <tr>
                        <td> %s</td>
                    </tr>
                    <tr>
                        <td>%s</td>
                    </tr>
                    <tr>
                        <td>%s</td>
                    </tr>
                </TABLE>>''' % (bcolor, marker, task, peopleName, dateDay))

            if(j > 1):
                if(marker != "Waiting"):
                    dot.edge(preorder, order)
                else:
                    dot.edge(preorder, order, color="white")

            j = j+1
        i = i+1

    # Rejected condition starts at here
    i = 1
    while(i < len(rows)-1):
        row_td = rows[i].find_all('td')
        str_cells = str(row_td[8])
        statusText = BeautifulSoup(str_cells, "lxml").get_text()
        status = str(statusText)
        if(status == "Completed- Rejected"):
            color = ""
            order = 'sturct'+str(j)
            preorder = 'sturct'+str(j-1)

            time_cell = str(row_td[7])
            time = BeautifulSoup(time_cell, "lxml").get_text()
            if("." in time):
                dateDay = time[:10]
                dateArr = dateDay.split(".")
                dateDay = dateArr[2]+"/"+dateArr[1]+"/"+dateArr[0]
            elif("/" in time):
                dateDay = time[:10]
                dateArr = dateDay.split("/")
                dateDay = dateArr[2]+"/"+dateArr[0]+"/"+dateArr[1]
            else:
                dateDay = time[:4]+"/"+time[4:6]+"/"+time[6:8]

            d0 = datetime.date.today()
            d1 = datetime.date(int(dateDay[0:4]), int(
                dateDay[5:7]), int(dateDay[8:]))
            delta = d0 - d1
            daypass = str(delta.days)
            print(daypass)

            task_cell = str(row_td[1])
            task = BeautifulSoup(task_cell, "lxml").get_text()
            task = task.replace("&", "and")
            print(task)

            people_name = str(row_td[2])
            people = BeautifulSoup(people_name, "lxml").get_text()
            peopleName = str(people)
            bcolor = "#C21807"

            dot.node(order, '''<
                <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
                    <tr >
                        <td colspan ="3" bgcolor='%s'>Rejected</td>
                    </tr>
                    <tr>
                        <td  rowspan = "4" ><img  src="C:\wrong.png" ></img></td>
                    </tr>
                    <tr>
                        <td colspan ="2"> %s</td>
                    </tr>
                    <tr>
                        <td>%s (<u><font color="blue">mailto:@dow.com</font></u>)</td>
                    </tr>
                    <tr>
                        <td colspan="2">%s</td>
                    </tr>

                </TABLE>>''' % (bcolor, task, peopleName, dateDay))
            dot.edge(preorder, order)

        i = i+1

    dot.edges(edge)
    output_stream = open(app.config['DOWNLOAD_FOLDER'] + filename, 'wb')
    dot.render(filename+'toPDF','pdf', view=True)



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

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
