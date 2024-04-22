import time
import csv,os

from flask import Flask
from flask import request,session, send_from_directory,make_response, render_template

import pymysql 
import json
import operator

from app import app

app = Flask(__name__, static_url_path='')


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/')
def home():
    #return '<b>hi</b>'
    data = {}
    data['x'] = [1,2,3,4,5,6,7,8,9,10]
    data['y'] = [5,7,3,1,5,8,7,3,9,1]
    return render_template('chart.html', title='Home', msg='Welcome!!!!',data=data)
#SELECT airlines.airline , COUNT(*) as num, HOUR(datapoints.date_time) as hr from datapoints LEFT JOIN flights ON datapoints.fid = flights.fid Left JOIN airlines ON flights.aid = airlines.aid GROUP BY hr;
@app.route('/getTopScorers')
def getTopScorers():
    #val = request.args.get("2022")
    url = 'http://127.0.0.1:5000/getTopScorers?season=2022&playoffs=1'
    data = json.loads(request.args.get(url))
    chart = {'x':[],'y':[]}
    for row in data:
        chart['x'].append(row['name'])
        chart['y'].append(int(row['goals']))
    return render_template('chart.html', title='Goals in a Season', msg='Welcome!!!!',data=chart)

    
@app.route('/selectairline')
def selectairline():
    conn = pymysql.connect(host='mysql.clarksonmsda.org', port=3306, user='ia626',
                       passwd='ia626clarkson', db='ia626', autocommit=True) #setup our credentials
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql ='SELECT * FROM airlines ORDER BY airline;'
    cur.execute(sql)
    airlines = []
    for row in cur:
        airline = {}
        airline['name'] = row['airline']
        airline['value'] = row['aid']
        airlines.append(airline)
    return render_template('selectairline.html',airlines=airlines)

@app.route('/csv')  
def download_csv():  
    csv = 'a,b,c\n1,2,3\n'  
    response = make_response(csv)
    cd = 'attachment; filename=mycsv.csv'
    response.headers['Content-Disposition'] = cd 
    response.mimetype='text/csv'

    return response


    
if __name__ == "__main__":
    app.run(host=os.getenv('HOSTIP', '127.0.0.1'),debug=os.getenv('FLASKDEBUG', True),port=os.getenv('PORT', '5001'))