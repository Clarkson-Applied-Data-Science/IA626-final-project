import time,requests
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
    season = request.args.get("season")
    playoffs = request.args.get("playoffs")
    url = f'http://127.0.0.1:5000/getTopScorers?season={season}&playoffs={playoffs}'
    r = requests.get(url)
    data = json.loads(r.text)
    chart = {'x':[],'y':[]}
    for row in data['rows']:
        chart['x'].append(row['name'])
        chart['y'].append(int(row['goals']))
    return render_template('getTopScorers.html', title='Goals in a Season', msg=f'The Top 10 Goal Scorers in {season}',data=chart)

@app.route('/getTeamShootingPct')
def getTeamShootingPct():
    season = request.args.get("season")
    playoffs = request.args.get("playoffs")
    url = f'http://127.0.0.1:5000/getTeamShootingPct?season={season}&playoffs={playoffs}'
    r = requests.get(url)
    data = json.loads(r.text)
    chart = {'x':[],'y':[]}
    for row in data['rows']:
        chart['x'].append(row['team'])
        chart['y'].append(float(row['shootingPct']))
    return render_template('getTeamShootingPct.html', title='Team Shooting Pct', msg=f'Teams Shooting % in {season}',data=chart) 

@app.route('/getPlayerChart')
def getPlayerChart():
    name = request.args.get("name")
    season = request.args.get("season")
    playoffs = request.args.get("playoffs")
    url = f'http://127.0.0.1:5000/getPlayerChart?name={name}&season={season}&playoffs={playoffs}'
    r = requests.get(url)
    data = json.loads(r.text)
    chart = {'x':[],'y':[],'x2':[],'y2':[],'x3':[],'y3':[]}
    for row in data['rows']:
        if row['event'] == 'MISS':
            chart['x'].append(int(row['xcord']))
            chart['y'].append(int(row['ycord']))
        if row['event'] == 'SHOT':
            chart['x2'].append(int(row['xcord']))
            chart['y2'].append(int(row['ycord']))
        if row['event'] == 'GOAL':
            chart['x3'].append(int(row['xcord']))
            chart['y3'].append(int(row['ycord']))
    return render_template('getPlayerChart.html', title='Player Shooting Chart', msg=f'{name} Shooting Chart in {season}',data=chart) 

@app.route('/selectseason')
def selectseason():
    conn = pymysql.connect(host='mysql.clarksonmsda.org', port=3306, user='ia626',
                       passwd='ia626clarkson', db='ia626', autocommit=True) #setup our credentials
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql ='SELECT season FROM geigersr_shots GROUP BY season ORDER BY season;'
    cur.execute(sql)
    seasons = []
    for row in cur:
        season = {}
        season['season'] = row['season']
        seasons.append(season)
    return render_template('selectairline.html',seasons=seasons)

if __name__ == "__main__":
    app.run(host=os.getenv('HOSTIP', '127.0.0.1'),debug=os.getenv('FLASKDEBUG', True),port=os.getenv('PORT', '5001'))