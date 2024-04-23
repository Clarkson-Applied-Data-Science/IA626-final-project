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
    return render_template('main.html', title='Home', msg='Welcome!!!!')

@app.route('/getPlayer')
def getPlayer():
    name = request.args.get("name")
    url = f'http://127.0.0.1:5000/getPlayer?name={name}'
    r = requests.get(url)
    data = json.loads(r.text)
    table = []
    table.append(list(data['rows'][0].keys()))
    for row in data['rows']:
        table.append(list(row.values()))
    return render_template('getPlayer.html', title='Goals in a Season', msg=f'Searched Name: {name}',data=table)

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

@app.route('/getAdvstats')
def getAdvstats():
    team = request.args.get("team")
    season = request.args.get("season")
    playoffs = request.args.get("playoffs")
    url = f'http://127.0.0.1:5000/getAdvstats?team={team}&season={season}&playoffs={playoffs}'
    r = requests.get(url)
    data = json.loads(r.text)
    table = []
    table.append(list(data['rows'][0]))
    for row in data['rows']:
        table.append(list(row.values()))
    return render_template('getAdvstats.html', title='Advanced Statistics', msg=f'{team} Stats in {season}',data=table)


if __name__ == "__main__":
    app.run(host=os.getenv('HOSTIP', '127.0.0.1'),debug=os.getenv('FLASKDEBUG', True),port=os.getenv('PORT', '5001'))