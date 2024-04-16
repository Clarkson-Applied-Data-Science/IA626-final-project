SELECT p.`name`,COUNT(s.`goal`) as `Goals`
FROM `geigersr_shots` s, `geigersr_players`p
WHERE p.`playerId` = s.`shooterId`
AND s.`goal` = 1
AND s.`season` = 2022 
GROUP BY s.`shooterId`
ORDER BY `Goals` DESC
LIMIT 0,10;


SELECT `teamCode`, ROUND(SUM(`goal`) / COUNT(`goal`) * 100,0) AS `shootingPct` 
FROM `geigersr_shots` 
WHERE `season` = %s
GROUP BY `teamCode` 
ORDER BY `ShootingPct` DESC;



SELECT s.`arenaAdjustedXCord`, s.`arenaAdjustedYCord`, s.`event`, p.`name`
FROM `geigersr_shots` s, `geigersr_players` p
WHERE s.`shooterId` = p.`playerId`
AND p.`name` = 'Connor McDavid'
AND s.`season` = 2022

SELECT event, shotType, count(*) 
FROM geigersr_shots
WHERE teamCode = 'NYI'
AND season = 2022
GROUP BY event,shotType
ORDER BY event

SELECT SUM(goal),SUM(shotGeneratedRebound),SUM(shotGoalieFroze), SUM(shotOnEmptyNet), SUM(shotRebound), SUM(shotRush),SUM(shotWasOnGoal)
FROM geigersr_shots 
WHERE teamCode = 'NYI'
AND season = 2022
AND isPlayoffGame = 0