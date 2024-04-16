SELECT p.`name`,COUNT(s.`goal`) as `Goals`
FROM `geigersr_shots` s, `geigersr_players`p
WHERE p.`playerId` = s.`shooterId`
AND s.`goal` = 1
AND s.`season` = 2022 
GROUP BY s.`shooterId`
ORDER BY `Goals` DESC
LIMIT 0,10;


