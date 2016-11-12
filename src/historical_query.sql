-- '''
-- Calculate historical average of teams
-- '''
-- SELECT fixtures.match_id,
--        fixtures.hometeam_id,
--        tmp_h.team as team_h,
--        tmp_h.avg_goals_h,
--        fixtures.awayteam_id,
--        tmp_a.team as team_a,
--        tmp_a.avg_goals_a
-- FROM fixtures
-- JOIN
-- (SELECT team, team_id, AVG(goals) AS avg_goals_h
-- FROM trans_fix
-- WHERE loc = 'home'
-- GROUP BY team, team_id)
-- AS tmp_h
-- ON tmp_h.team_id = fixtures.hometeam_id
-- JOIN
-- (SELECT team, team_id, AVG(goals) AS avg_goals_a
-- FROM trans_fix
-- WHERE loc = 'away'
-- GROUP BY team, team_id)
-- AS tmp_a
-- ON tmp_a.team_id = fixtures.awayteam_id
-- ORDER BY fixtures.match_id DESC
-- LIMIT 10;

-- Calculate historical average of teams
-- and create model_table
DROP TABLE fixtures_history;

CREATE TABLE fixtures_history
AS
SELECT fixtures.match_id,
       fixtures.hometeam_id,
       tmp_h.team as team_h,
       tmp_h.avg_goals_h,
       fixtures.awayteam_id,
       tmp_a.team as team_a,
       tmp_a.avg_goals_a
FROM fixtures
JOIN
(SELECT team, team_id, AVG(goals) AS avg_goals_h
FROM trans_fix
WHERE loc = 'home'
GROUP BY team, team_id)
AS tmp_h
ON tmp_h.team_id = fixtures.hometeam_id
JOIN
(SELECT team, team_id, AVG(goals) AS avg_goals_a
FROM trans_fix
WHERE loc = 'away'
GROUP BY team, team_id)
AS tmp_a
ON tmp_a.team_id = fixtures.awayteam_id;
