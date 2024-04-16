import json,pymysql,time
from flask import Flask
from flask import request,redirect

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
        res['msg'] = 'Please Enter a Valid NHL Player Name'
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
        res['msg'] = 'Please Enter a Year between 2007 and 2022'
        res['rows'] = None
    return json.dumps(res,indent=4)

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True)