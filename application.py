from flask import Flask, request, jsonify, Response, send_file
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os
import sys
from bs4 import BeautifulSoup
import lxml.html as lh
import datetime
import json

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'

app = Flask(__name__)        
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# POST - just get the image and metadata

@app.route('/hi')
def hi():
    return 'hello, world!'

@app.route('/get_image')
def get_image():
    if request.args.get('type') == '1':
       filename = 'https://github.com/liuw888/test/blob/master/ok.png'
    else:
       filename = 'https://github.com/liuw888/test/blob/master/wrong.png'
    return send_file(filename, mimetype='image/gif')


@app.route('/request', methods=['POST'])
def post():
    file = request.files.get('htmlfile', '')
    filename = secure_filename(file.filename)
    #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #return '''<h1>file is received: {}</h1>'''.format(filename)
    #print('saved',file = sys.stderr)
    #print(filename,file = sys.stderr)
    content = file.read()
    #content= open(os.path.join(app.config['UPLOAD_FOLDER'], filename)).read()
    #print(content,file = sys.stderr)
    #print('content', file=sys.stderr)
    soup = BeautifulSoup(content, 'lxml')
    rows = soup.find_all('tr')
    #return '''{}'''.format(rows[1])
    
    #dot language starts here!
    i = 1
    edge = []
    j = 1
    row_td = rows[0].find_all('td')
    header=['']*len(row_td)
    print(len(row_td))
    res =  ' graph{  node [shape=plaintext]; ' 
    for x in range( len(row_td)-1):
        header[x] = BeautifulSoup(str(row_td[x]), "lxml").get_text()
    print(header[:7])
    
    while(i < len(rows)-1):
        row_td = rows[i].find_all('td')
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
                res+= chr(j+65) + ''' [label=< \n
                <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="8">
                        <tr >
                            <td colspan ="4" bgcolor='%s'>Waiting</td>
                        </tr>
                        <tr>
                            <td rowspan ="3" colspan ="3" >Waiting</td>
                        </tr>
                        <tr>
                            <td>%s</td>
                        </tr>
                        <tr>
                            <td>%s</td>
                        </tr>
                </TABLE>>];\n''' % (bcolor, task, peopleName)

            elif(marker == "Completed"):
                

                res += chr(j+65) + ''' [label=< \n
                <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
                        <tr >
                            <td colspan ="4" bgcolor='%s'>Completed</td>
                        </tr>
                        <tr>
                            <td rowspan ="4" colspan ="3" >Yes</td>
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
                </TABLE>>];\n''' % (bcolor, task, peopleName, dateDay)

            elif("Pending" in marker):
                res += chr(j+65) + ''' [label=< \n
                <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="8">
                    <tr >
                        <td colspan ="4" bgcolor='%s'>%s</td>
                    </tr>
                    <tr>
                        <td rowspan ="4" colspan ="3" >Pending</td>
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
                </TABLE>>];\n''' % (bcolor, marker, task, peopleName, dateDay)

            elif(marker == "Staff failure"):
                res += chr(j+65) +''' [label=< \n
                <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
                    <tr >
                        <td colspan ="4" bgcolor='%s'>%s</td>
                    </tr>
                    <tr>
                        <td rowspan ="5" colspan ="3" >staff</td>
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
                </TABLE>>];\n''' % (bcolor, marker, task, peopleName, dateDay)

            else:
                res += chr(j+65) +''' [label=< \n
                <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
                    <tr >
                        <td colspan ="4" bgcolor='%s'>%s</td>
                    </tr>
                    <tr>
                        <td rowspan ="4" colspan ="3" >No</td>
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
                </TABLE>>];\n''' % (bcolor, marker, task, peopleName, dateDay)

            

            j = j+1
        i = i+1

    # # Rejected condition starts at here
    # i = 1
    # while(i < len(rows)-1):
    #     row_td = rows[i].find_all('td')
    #     str_cells = str(row_td[8])
    #     statusText = BeautifulSoup(str_cells, "lxml").get_text()
    #     status = str(statusText)
    #     if(status == "Completed- Rejected"):
    #         color = ""
    #         order = 'sturct'+str(j)
    #         preorder = 'sturct'+str(j-1)

    #         time_cell = str(row_td[7])
    #         time = BeautifulSoup(time_cell, "lxml").get_text()
    #         if("." in time):
    #             dateDay = time[:10]
    #             dateArr = dateDay.split(".")
    #             dateDay = dateArr[2]+"/"+dateArr[1]+"/"+dateArr[0]
    #         elif("/" in time):
    #             dateDay = time[:10]
    #             dateArr = dateDay.split("/")
    #             dateDay = dateArr[2]+"/"+dateArr[0]+"/"+dateArr[1]
    #         else:
    #             dateDay = time[:4]+"/"+time[4:6]+"/"+time[6:8]

    #         d0 = datetime.date.today()
    #         d1 = datetime.date(int(dateDay[0:4]), int(
    #             dateDay[5:7]), int(dateDay[8:]))
    #         delta = d0 - d1
    #         daypass = str(delta.days)
    #         print(daypass)

    #         task_cell = str(row_td[1])
    #         task = BeautifulSoup(task_cell, "lxml").get_text()
    #         task = task.replace("&", "and")
    #         print(task)

    #         people_name = str(row_td[2])
    #         people = BeautifulSoup(people_name, "lxml").get_text()
    #         peopleName = str(people)
    #         bcolor = "#C21807"

    #         dot.node(order, '''<
    #             <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
    #                 <tr >
    #                     <td colspan ="3" bgcolor='%s'>Rejected</td>
    #                 </tr>
    #                 <tr>
    #                     <td  rowspan = "4" ><img  src="C:\wrong.png" ></img></td>
    #                 </tr>
    #                 <tr>
    #                     <td colspan ="2"> %s</td>
    #                 </tr>
    #                 <tr>
    #                     <td>%s (<u><font color="blue">mailto:@dow.com</font></u>)</td>
    #                 </tr>
    #                 <tr>
    #                     <td colspan="2">%s</td>
    #                 </tr>

    #             </TABLE>>''' % (bcolor, task, peopleName, dateDay))
    #         dot.edge(preorder, order)

    #     i = i+1
    res += '}';

    js = json.dumps(res);
    resp = Response(js, status=200, mimetype='application/json')
    return resp;


@app.route('/test', methods=['POST','GET'])
def test():
    if request.method == 'POST':
        language = request.form.get('language')
        framework = request.form['framework']
        return '''<h1> language is:{}</h1>
            <h1>framework is: {}</h1>'''.format(language,framework)

    return '''<form method="POST">
                Language: <input type="text" name="language"><br>
                Framework: <input type="text" name="framework"><br>
                <input type="submit" value="Submit"><br>
              </form>'''

@app.route('/havefun', methods=['POST','GET'])
def havefun():
    if request.method == 'POST':
        language = request.form.get('language')
        return '''<h1> You jsu said{}</h1>
            <h1>but I don't care, I would like to say I love you</h1>
            '''.format(language)

    return '''<form method="POST">
                Say something at here: <input type="text" name="language"><br>
                <input type="submit" value="Submit"><br>
              </form>'''
    

if __name__ == "__main__":
    app.run(debug=True)
