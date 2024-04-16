import json,pymysql,time
from flask import Flask
from flask import request,redirect
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)
res = {}
@app.route("/", methods=['GET','POST'])
def root():
    res['code'] = 2
    res['msg'] = "No endpoint specifed"
    res['req'] = '/'
    return json.dumps(res,indent=4)

@app.route("/getPlayer", methods=['GET','POST'])
def getPlayer():
    conn = pymysql.connect(host='mysql.clarksonmsda.org',port=3306,user='ia626',passwd='ia626clarkson', db='ia626', autocommit=True)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql = '''SELECT * FROM `geigersr_players` WHERE `name` like %s LIMIT 0,10;'''
    name = request.args.get('name')
    print(name)
    token = f"%{name}%"
    cur.execute(sql,(token))
    rows = []
    for row in cur:
        d = {}
        d['playerId'] = row['playerId']
        d['name'] = row['name']
        d['position'] = row['position']
        d['birthDate'] = str(row['birthDate'])
        d['weight'] = row['weight']
        d['height'] = row['height']
        d['nationality'] = row['nationality']
        d['shootsCatches'] = row['shootsCatches']
        d['primaryNumber'] = row['primaryNumber']
        rows.append(d)
    if len(rows) > 0:
        res['code'] = 1
        res['msg'] = 'ok'
        res['req'] = '/getPlayer'
        res['rows'] = rows
    else:
        res['code'] = 0
        res['msg'] = 'Please enter a valid NHL player name'
        res['rows'] = None
    return json.dumps(res,indent=4)

@app.route("/getTopScorers", methods=['GET','POST'])
def getTopScorers():
    conn = pymysql.connect(host='mysql.clarksonmsda.org',port=3306,user='ia626',passwd='ia626clarkson', db='ia626', autocommit=True)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql = '''SELECT p.`name`,COUNT(s.`goal`) as `goals` FROM `geigersr_shots` s, `geigersr_players`p WHERE p.`playerId` = s.`shooterId`
                AND s.`goal` = 1 AND s.`season` = %s GROUP BY s.`shooterId` ORDER BY `Goals` DESC LIMIT 0,10;'''
    season = request.args.get('season')
    print(season)
    token = f"{season}"
    cur.execute(sql,(token))
    rows = []
    for row in cur:
        d = {}
        d['name'] = row['name']
        d['goals'] = row['goals']
        rows.append(d)
    if len(rows) > 0:
        res['code'] = 1
        res['msg'] = 'ok'
        res['req'] = '/getTopScorers'
        res['rows'] = rows
    else:
        res['code'] = 0
        res['msg'] = 'Please enter a year between 2007 and 2022'
        res['rows'] = None
    return json.dumps(res,indent=4)

@app.route("/getTeamShootingPct", methods=['GET','POST'])
def getTeamShootingPct():
    conn = pymysql.connect(host='mysql.clarksonmsda.org',port=3306,user='ia626',passwd='ia626clarkson', db='ia626', autocommit=True)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql = '''SELECT `teamCode`, ROUND(SUM(`goal`) / COUNT(`goal`) * 100,0) AS `shootingPct` FROM `geigersr_shots` WHERE `season` = %s
                GROUP BY `teamCode` ORDER BY `ShootingPct` DESC;'''
    season = request.args.get('season')
    print(season)
    token = f"{season}"
    cur.execute(sql,(token))
    rows = []
    for row in cur:
        d = {}
        d['team'] = row['teamCode']
        d['shootingPct'] = int(row['shootingPct']) 
        rows.append(d)
    if len(rows) > 0:
        res['code'] = 1
        res['msg'] = 'ok'
        res['req'] = '/getTeamShootingPct'
        res['rows'] = rows
    else:
        res['code'] = 0
        res['msg'] = 'Please enter a year between 2007 and 2022'
        res['rows'] = None
    return json.dumps(res,indent=4)

@app.route("/getPlayerChart", methods=['GET','POST'])
def getPlayerChart():
    conn = pymysql.connect(host='mysql.clarksonmsda.org',port=3306,user='ia626',passwd='ia626clarkson', db='ia626', autocommit=True)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql = '''SELECT s.arenaAdjustedXCord, s.arenaAdjustedYCord, s.event, p.name FROM geigersr_shots s, geigersr_players p
            WHERE s.shooterId = p.playerId AND p.name = %s AND s.season = %s;'''
    name = request.args.get('name')
    season = request.args.get('season')
    print(name, season)
    tokens = [name, season]
    cur.execute(sql,(tokens))
    rows = []
    for row in cur:
        d = {}
        d['xcord'] = row['arenaAdjustedXCord']
        d['ycord'] = row['arenaAdjustedYCord']
        d['event'] = row['event']
        d['name'] = row['name']
        rows.append(d)
    
    if len(rows) > 0:
        res['code'] = 1
        res['msg'] = 'ok'
        res['req'] = '/getPlayerChart'
        res['rows'] = rows

    else:
        res['code'] = 0
        res['msg'] = 'Please enter a year between 2007 and 2022 and a valid NHL player name'
        res['rows'] = None
    return json.dumps(res,indent=4)

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True)