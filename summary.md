# NHL Player Shot API
### By Sebastian Geiger

## Summary/Initial Question
For my project I want to look more in depth into NHL statistics. I was able to find a dataset that has every single shot taken in an NHL game from 2007-2022. This dataset includes where on the ice the shot was taken from, who the shooter was, the type of shot that was taken and also information about the play around the shooter. My initial question was is there any correlation between any of these shot characteristics and the probability of a goal being scored at a given time. Hockey is a very fast game with a constant flow of play. This makes it difficult to get advanced statistics on parts of the game, unlike other sports like baseball or football that have set pitches and plays that divide the game up into even segments. I wanted to see what players not only generate the most shots, but the highest quality shots based on location, angle, and situation. My goal is to take two flat csv files that contain player descriptions and shot data and turn them into a API that can be utilized by users to gather valuable information about their favorite players. My API will have multiple endpoints that query the data to show different metrics for different groups of players as well as indiviual players over the provided years. 

## Outline

#### mysql loading
The first step is to get the csv data that I want to use into a mysql database. I did this by writing a python script to import two tables based on the schema below. The `players` table was simple to enter and I was able to load the table into mysql with ease, only needing to make a date conversion for the `birthDate` field. The 'shots' table did not have any date requirements, but it did have some challenges. Based on the schema below, the `shots` table has two foreign keys that connect to the `playerId` in the `players` table. In the to csv files that I pulled the data from the `playerId` fields had different types. In the player csv, the field was read in by python as a interger type, but in the shots datafile, the `shooterPlayerId` and `goalieIdForShot` fields read in as a string with a trailing decimal and zero. This caused a foreign key constraint error to arise due to the Ids not aligning. To fix this I changed the mysql field type to char(7) then added a few lines of cude to cut the '.0' off the end of the Ids, so they aligned with the other table.  
!['schema'](mysqlschema.png)
The next step would then be to translate the mysql tables into a json format to be used for the API.

#### Developing API

#### Interface and Graphs

## Python Code
#### 'geigersr_players' Table Creation and Insertion
```
import pymysql, csv, time
import datetime
with open('allPlayersLookup.csv') as f:
    data = [{k: str(v) for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]

conn = pymysql.connect(host='mysql.clarksonmsda.org', port=3306, user='ia626',
                       passwd='ia626clarkson', db='ia626', autocommit=True) 
cur = conn.cursor(pymysql.cursors.DictCursor)
cur.execute("DROP TABLE IF EXISTS `geigersr_shots`;")
cur.execute("DROP TABLE IF EXISTS `geigersr_players`;")
sql = """CREATE TABLE `geigersr_players`
(
  `playerId` CHAR(7) NOT NULL,
  `name` VARCHAR(30) NOT NULL,
  `position` CHAR(1) NULL,
  `birthDate` DATE NULL,
  `weight` varchar(3) NULL,
  `height` VARCHAR(8) NULL,
  `nationality` CHAR(3) NULL,
  `shootsCatches` CHAR(1) NULL,
  `primaryNumber` varchar(2) NULL,
  `primaryPosition` CHAR(1) NULL,
  PRIMARY KEY (`playerId`)
);"""
cur.execute(sql)
sql = '''INSERT INTO `geigersr_players` (`playerId`,`name`,`position`,`birthDate`,`weight`,`height`,`nationality`,
  `shootsCatches`,`primaryNumber`,`primaryPosition`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
n = 0
blocksize = 500
tokens = []
for row in data:
    dto = None
    try:
        dto = datetime.datetime.strptime(row['birthDate'],"%m/%d/%Y")
    except Exception as e:
        #print(e)
        pass
    if dto is not None:
        dts = dto.strftime("%Y-%m-%d")
    else:
        dts = None
    tokens.append([row['playerId'],row['name'],row['position'],dts,
                    row['weight'],row['height'],row['nationality'],row['shootsCatches'],
                    row['primaryNumber'],row['primaryPosition']])
    if len(tokens) >= blocksize:
        cur.executemany(sql,tokens)
        tokens = []
    if n % 1000 == 0:
        print(n)
    n += 1
if len(tokens) > 0:
    cur.executemany(sql, tokens)
```
#### 'geigersr_shots' Table Creation and Insertion
```
cur.execute("DROP TABLE IF EXISTS `geigersr_shots`;")
sql = ''' CREATE TABLE `geigersr_shots`
(
  `shotID` INT NOT NULL,
  `arenaAdjustedXCord` INT NOT NULL,
  `arenaAdjustedYCord` INT NOT NULL,
  `averageRestDifference` NUMERIC(7,2) NOT NULL,
  `event` VARCHAR(5) NOT NULL,
  `game_id` INT NOT NULL,
  `goal` INT NOT NULL,
  `isPlayoffGame` INT NOT NULL,
  `lastEventCategory` VARCHAR(10) NOT NULL,
  `season` INT NOT NULL,
  `shotAngle` NUMERIC(11,9) NOT NULL,
  `shotDistance` NUMERIC(12,9) NOT NULL,
  `shotGeneratedRebound` INT NOT NULL,
  `shotGoalieFroze` INT NOT NULL,
  `shotOnEmptyNet` INT NOT NULL,
  `shotRebound` INT NOT NULL,
  `shotRush` INT NOT NULL,
  `shotType` VARCHAR(10) NOT NULL,
  `shotWasOnGoal` INT NOT NULL,
  `team` CHAR(4) NOT NULL,
  `teamCode` CHAR(3) NOT NULL,
  `time` INT NOT NULL,
  `goalieId` char(7) NOT NULL,
  `shooterId` char(7) NOT NULL,
  PRIMARY KEY (`shotid`),
  FOREIGN KEY (`goalieId`) REFERENCES `geigersr_players`(`playerId`),
  FOREIGN KEY (`shooterId`) REFERENCES `geigersr_players`(`playerId`)
);  '''
cur.execute(sql)
sql = '''INSERT INTO `geigersr_shots` ( `shotID`,`arenaAdjustedXCord`,`arenaAdjustedYCord`,`averageRestDifference`,`event`,
  `game_id`,`goal`,`isPlayoffGame`,`lastEventCategory`,`season`,`shotAngle`,`shotDistance`,`shotGeneratedRebound`,
  `shotGoalieFroze`,`shotOnEmptyNet`,`shotRebound`,`shotRush`,`shotType`,`shotWasOnGoal`,`team`,`teamCode`,`time`,`goalieId`,
  `shooterId`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
n = 0
blocksize = 500
tokens = []
for row in data:
    shooter = row['shooterPlayerId']
    shooter2 = id.split('.')
    shooterid = shooter2[0]
    goalie = row['goalieIdForShot']
    goalie2 = id.split('.')
    goalieid = shooter2[0]
    tokens.append([row['shotID'],row['arenaAdjustedXCord'],row['arenaAdjustedYCord'],row['averageRestDifference'],row['event'],
                    row['game_id'],row['goal'],row['isPlayoffGame'],row['lastEventCategory'], row['season'], row['shotAngle'],
                    row['shotDistance'],row['shotGeneratedRebound'],row['shotGoalieFroze'], row['shotOnEmptyNet'],
                    row['shotRebound'],row['shotRush'],row['shotType'],row['shotWasOnGoal'],row['team'],row['teamCode'],
                    row['time'],goalieid,shooterid])
    if len(tokens) >= blocksize:
        cur.executemany(sql,tokens)
        tokens = []
    if n % 10000 == 0:
        print(n)
    n += 1
if len(tokens) > 0:
    cur.executemany(sql, tokens)
```

## Figures


## Results


# Code/API appendix