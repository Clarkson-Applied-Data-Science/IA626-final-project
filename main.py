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
    return render_template('getPlayer.html', title=f'{name}', msg=f'Searched Name: {name}',data=table, name=name)

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
    return render_template('getTopScorers.html', title='Top Goal Scorers', msg=f'The Top 10 Goal Scorers in {season}',data=chart)

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
    return render_template('getAdvstats.html', title='Advanced Statistics', msg=f'{team} Stats in {season}',data=table, name=team)

@app.route('/selectPlayer')
def selectPlayer():
    conn = pymysql.connect(host='mysql.clarksonmsda.org', port=3306, user='ia626',
                       passwd='ia626clarkson', db='ia626', autocommit=True) #setup our credentials
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql ='SELECT * FROM geigersr_players ORDER BY name;'
    cur.execute(sql)
    players = []
    for row in cur:
        player = {}
        player['name'] = row['name']
        players.append(player)
    return render_template('selectPlayer.html',players=players)

@app.route('/selectSeason')
def selectSeason():
    conn = pymysql.connect(host='mysql.clarksonmsda.org', port=3306, user='ia626',
                       passwd='ia626clarkson', db='ia626', autocommit=True) #setup our credentials
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql ='SELECT season FROM geigersr_shots GROUP BY season ORDER BY season DESC;'
    cur.execute(sql)
    seasons = []
    for row in cur:
        season = {}
        season['season'] = row['season']
        seasons.append(season)
    sql ='SELECT isPlayoffGame FROM geigersr_shots GROUP BY isPlayoffGame ORDER BY isPlayoffGame;'
    cur.execute(sql)
    playoffs = []
    for row in cur:
        playoff = {}
        playoff['playoff'] = row['isPlayoffGame']
        playoffs.append(playoff)
    return render_template('selectSeason.html',seasons=seasons, playoffs=playoffs)

@app.route('/selectSeason2')
def selectSeason2():
    conn = pymysql.connect(host='mysql.clarksonmsda.org', port=3306, user='ia626',
                       passwd='ia626clarkson', db='ia626', autocommit=True) #setup our credentials
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql ='SELECT season FROM geigersr_shots GROUP BY season ORDER BY season DESC;'
    cur.execute(sql)
    seasons = []
    for row in cur:
        season = {}
        season['season'] = row['season']
        seasons.append(season)
    sql ='SELECT isPlayoffGame FROM geigersr_shots GROUP BY isPlayoffGame ORDER BY isPlayoffGame;'
    cur.execute(sql)
    playoffs = []
    for row in cur:
        playoff = {}
        playoff['playoff'] = row['isPlayoffGame']
        playoffs.append(playoff)
    return render_template('selectSeason2.html',seasons=seasons, playoffs=playoffs)

@app.route('/selectPlayerSeason')
def selectPlayerSeason():
    conn = pymysql.connect(host='mysql.clarksonmsda.org', port=3306, user='ia626',
                       passwd='ia626clarkson', db='ia626', autocommit=True) #setup our credentials
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql ='SELECT season FROM geigersr_shots GROUP BY season ORDER BY season DESC;'
    cur.execute(sql)
    seasons = []
    for row in cur:
        season = {}
        season['season'] = row['season']
        seasons.append(season)
    sql ='SELECT isPlayoffGame FROM geigersr_shots GROUP BY isPlayoffGame ORDER BY isPlayoffGame;'
    cur.execute(sql)
    playoffs = []
    for row in cur:
        playoff = {}
        playoff['playoff'] = row['isPlayoffGame']
        playoffs.append(playoff)
    sql ='SELECT * FROM geigersr_players ORDER BY name;'
    cur.execute(sql)
    players = []
    for row in cur:
        player = {}
        player['name'] = row['name']
        players.append(player)
    return render_template('selectPlayerSeason.html',seasons=seasons, playoffs=playoffs, players=players)

@app.route('/selectTeamSeason')
def selectTeamSeason():
    conn = pymysql.connect(host='mysql.clarksonmsda.org', port=3306, user='ia626',
                       passwd='ia626clarkson', db='ia626', autocommit=True) #setup our credentials
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql ='SELECT season FROM geigersr_shots GROUP BY season ORDER BY season DESC;'
    cur.execute(sql)
    seasons = []
    for row in cur:
        season = {}
        season['season'] = row['season']
        seasons.append(season)
    sql ='SELECT isPlayoffGame FROM geigersr_shots GROUP BY isPlayoffGame ORDER BY isPlayoffGame;'
    cur.execute(sql)
    playoffs = []
    for row in cur:
        playoff = {}
        playoff['playoff'] = row['isPlayoffGame']
        playoffs.append(playoff)
    sql ='SELECT teamCode FROM geigersr_shots GROUP BY teamCode ORDER BY teamCode;'
    cur.execute(sql)
    teams = []
    for row in cur:
        team = {}
        team['team'] = row['teamCode']
        teams.append(team)
    return render_template('selectTeamSeason.html',seasons=seasons, playoffs=playoffs, teams=teams)

if __name__ == "__main__":
    app.run(host=os.getenv('HOSTIP', '127.0.0.1'),debug=os.getenv('FLASKDEBUG', True),port=os.getenv('PORT', '5001'))