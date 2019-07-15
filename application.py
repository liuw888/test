from flask import Flask, request, jsonify, Response, render_template

from werkzeug.utils import secure_filename
import os
import sys
from bs4 import BeautifulSoup
import lxml.html as lh
import datetime

app = Flask(__name__)        

@app.route('/')
def homepage():
    return 'Welcome to the homepage'


@app.route('/run', methods=['POST','GET'])
def run():
    if request.method == 'POST':
        
        #upload and read file
        file = request.files['htmlfile']
        filename = secure_filename(file.filename)
        content = file.read()
        soup = BeautifulSoup(content, 'lxml')
        rows = soup.find_all('tr')
        
        #drawing tables
        last =0
        i = 1
        edge = []
        j = 1
        count = 1
        res =""
        row_td = rows[0].find_all('td')
        header=['']*len(row_td)
        print(len(row_td))
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

                if(status == 'Completed- Successfully'):
                    marker = "Completed"
                    bcolor = "#98FB98"
                    img = "https://github.com/liuw888/test/blob/master/ok.png?raw=true"
                elif(status == 'Released- Notified'):
                    marker = "Pending %s days" % daypass
                    bcolor = "#FFA500"
                    img = "https://github.com/liuw888/test/blob/master/working.png?raw=true"
                elif(status == 'Released- Waiting' or status == 'Released'):
                    marker = "Waiting"
                    bcolor = "#FADA5E"
                    img = "https://github.com/liuw888/test/blob/master/waiting.png?raw=true"
                elif(status == "Completed- Aborted"):
                    marker = "Aborted"
                    bcolor = "#C21807"
                    img ="https://github.com/liuw888/test/blob/master/wrong.png?raw=true"
                elif (status == "Completed- Staffing Failure"):
                    marker = "Staff failure"
                    bcolor = "#C21807"
                    img ="https://github.com/liuw888/test/blob/master/Staff%20failure.png?raw=true"

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
                    res+= '''
                    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="8" style="float: left;" align="center" >
                            <tr >
                                <td colspan ="4" bgcolor='%s' align="center">Waiting</td>
                            </tr>
                            <tr>
                                <td rowspan ="3" colspan ="2" ><img src = %s></img></td>
                            </tr>
                            <tr>
                                <td align="center">%s</td>
                            </tr>
                            <tr>
                                <td align="center">%s</td>
                            </tr>
                    </TABLE> ''' % (bcolor,img, task, peopleName)
 
                elif(marker == "Completed"):
                    res  = constructTable(res,bcolor, marker,img, task, peopleName, dateDay)
                    last = j+65

                elif("Pending" in marker):
                    res =constructTable(res,bcolor, marker,img, task, peopleName, dateDay)
                    last = j+65
                    # res = res +  chr(j+65) +'->'+chr(j+66)+'   '

                elif(marker == "Staff failure"):
                    res =constructTable (res,bcolor, marker,img, task, peopleName, dateDay)
                    last = j+65
                    # For support: <u><font color="blue">http://manage-info.intranet.dow.com/Forms/DS/DS-MMD/F_DS_MMD-MSOR.asp</font></u>
                    # res = res +  chr(j+65) +'->'+chr(j+66)+'   '

                else: #aborted
                    res = constructTable (res,bcolor, marker,img, task, peopleName, dateDay)
                j = j+1
            i = i+1
        

        i = 1
    while(i < len(rows)-1):
        row_td = rows[i].find_all('td')
        str_cells = str(row_td[8])
        statusText = BeautifulSoup(str_cells, "lxml").get_text()
        status = str(statusText)
        if(status == "Completed- Rejected"):
            marker = "Rejected"
            color = ""

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
            img =" https://github.com/liuw888/test/blob/master/wrong.png?raw=true"

            res = constructTable(res,bcolor, marker,img, task, peopleName, dateDay)

        return render_template("index2.html",tablecontent=res)

    return render_template("index.html")


def constructTable(res,bcolor, marker,img, task, peopleName, dateDay):
    res += '''<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4" align="center">
                    <tr >
                        <td colspan ="3" bgcolor='%s'align="center">%s</td>
                    </tr>
                    <tr>
                        <td  rowspan = "4"><img src = %s></img></td>
                    </tr>
                    <tr>
                        <td colspan ="2"align="center"> %s</td>
                    </tr>
                    <tr>
                        <td align="center">%s</td>
                    </tr>
                    <tr>
                        <td colspan="2" align="center">%s</td>
                    </tr>
                </TABLE>
                <p align="center"><font size="6">&darr;</font></p>''' % (bcolor, marker, img, task, peopleName, dateDay)
    return res; 

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




# @app.route('/test', methods=['POST','GET'])
# def test():
#     if request.method == 'POST':
#         language = request.form.get('language')
#         framework = request.form['framework']
#         return '''<h1> language is:{}</h1>
#             <h1>framework is: {}</h1>'''.format(language,framework)

#     return '''<form method="POST">
#                 Language: <input type="text" name="language"><br>
#                 Framework: <input type="text" name="framework"><br>
#                 <input type="submit" value="Submit"><br>
#               </form>'''
