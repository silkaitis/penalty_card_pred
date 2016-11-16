CREATE TEMPORARY TABLE temp_ref AS
SELECT *
FROM ref_details;

ALTER TABLE temp_ref
DROP COLUMN id,
DROP COLUMN match_date,
DROP COLUMN hometeam,
DROP COLUMN hometeam_id,
DROP COLUMN homegoals,
DROP COLUMN awayteam,
DROP COLUMN awayteam_id,
DROP COLUMN awaygoals,
DROP COLUMN single_yellow,
DROP COLUMN double_yellow,
DROP COLUMN red,
DROP COLUMN ref_name;

CREATE TEMPORARY TABLE temp_fix AS
SELECT *
FROM fixtures;

DROP TABLE IF EXISTS fixtures_full;

CREATE TABLE fixtures_full AS
SELECT *
FROM temp_fix
JOIN temp_ref
USING (match_id);

DROP TABLE temp_ref;
DROP TABLE temp_fix;
