-- Create temporary tables to drop unwanted info
CREATE TEMPORARY TABLE temp_history AS
SELECT *
FROM fixtures_history;

ALTER TABLE temp_history
DROP COLUMN hometeam_id,
DROP COLUMN team_h,
DROP COLUMN awayteam_id,
DROP COLUMN team_a;

CREATE TEMPORARY TABLE temp_sum AS
SELECT *
FROM fixtures_sum;

ALTER TABLE temp_sum
DROP COLUMN awayteam_id,
DROP COLUMN awayteam,
DROP COLUMN hometeam_id,
DROP COLUMN hometeam,
DROP COLUMN date,
DROP COLUMN season;

DROP TABLE IF EXISTS base_table;

CREATE TABLE base_table AS
SELECT *
FROM temp_sum
JOIN temp_history
USING (match_id);

DROP TABLE temp_sum;
DROP TABLE temp_history;
