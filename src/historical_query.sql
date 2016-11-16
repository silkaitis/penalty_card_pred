DROP TABLE IF EXISTS fixtures_history;

CREATE TABLE fixtures_history
AS
SELECT fixtures_full.match_id,
       fixtures_full.ref_id,
       fixtures_full.hometeam_id,
       tmp_h.team as team_h,
       tmp_h.avg_corners_h,
       tmp_h.avg_fouls_h,
       tmp_h.avg_goals_h,
       tmp_h.avg_goalsa_h,
       tmp_h.avg_red_h,
       tmp_h.avg_yellow_h,
       tmp_h.avg_shots_h,
       tmp_h.avg_sot_h,
       fixtures_full.awayteam_id,
       tmp_a.team as team_a,
       tmp_a.avg_corners_a,
       tmp_a.avg_fouls_a,
       tmp_a.avg_goals_a,
       tmp_a.avg_goalsa_a,
       tmp_a.avg_red_a,
       tmp_a.avg_yellow_a,
       tmp_a.avg_shots_a,
       tmp_a.avg_sot_a,
       tmp_rh.ref_avg_yh,
       tmp_ra.ref_avg_ya,
       tmp_rh.ref_avg_rh,
       tmp_ra.ref_avg_ra,
       hth.hth_ca,
       hth.hth_fa,
       hth.hth_ga,
       hth.hth_gaa,
       hth.hth_ra,
       hth.hth_sa,
       hth.hth_sota,
       hth.hth_ya,
       hth.hth_htga,
       hth.hth_ch,
       hth.hth_fh,
       hth.hth_gh,
       hth.hth_gah,
       hth.hth_rh,
       hth.hth_sh,
       hth.hth_soth,
       hth.hth_yh,
       hth.hth_htgh
FROM fixtures_full
JOIN
(SELECT team,
  team_id,
  AVG(corners) AS avg_corners_h,
  AVG(fouls) AS avg_fouls_h,
  AVG(goals) AS avg_goals_h,
  AVG(goalsallowed) AS avg_goalsa_h,
  AVG(redcards) AS avg_red_h,
  AVG(yellowcards) AS avg_yellow_h,
  AVG(shots) AS avg_shots_h,
  AVG(shotsontarget) AS avg_sot_h
FROM trans_fix
WHERE loc = 'home'
GROUP BY team, team_id)
AS tmp_h
ON tmp_h.team_id = fixtures_full.hometeam_id

JOIN
(SELECT team,
  team_id,
  AVG(corners) AS avg_corners_a,
  AVG(fouls) AS avg_fouls_a,
  AVG(goals) AS avg_goals_a,
  AVG(goalsallowed) AS avg_goalsa_a,
  AVG(redcards) AS avg_red_a,
  AVG(yellowcards) AS avg_yellow_a,
  AVG(shots) AS avg_shots_a,
  AVG(shotsontarget) AS avg_sot_a
FROM trans_fix
WHERE loc = 'away'
GROUP BY team, team_id)
AS tmp_a
ON tmp_a.team_id = fixtures_full.awayteam_id

JOIN
(SELECT ref_id, team_id, loc, ref_avg_y AS ref_avg_yh, ref_avg_r AS ref_avg_rh
FROM
(SELECT ref_id, team_id, loc, avg(yellowcards) AS ref_avg_y, avg(redcards) AS ref_avg_r
FROM trans_fix
GROUP BY ref_id, team_id, loc) AS tmp_r
WHERE loc = 'home') AS tmp_rh
ON (tmp_rh.ref_id = fixtures_full.ref_id) AND (tmp_rh.team_id = fixtures_full.hometeam_id)

JOIN
(SELECT ref_id, team_id, loc, ref_avg_y AS ref_avg_ya, ref_avg_r AS ref_avg_ra
FROM
(SELECT ref_id, team_id, loc, avg(yellowcards) AS ref_avg_y, avg(redcards) AS ref_avg_r
FROM trans_fix
GROUP BY ref_id, team_id, loc) AS tmp_r
WHERE loc = 'away') AS tmp_ra
ON (tmp_ra.ref_id = fixtures_full.ref_id) AND (tmp_ra.team_id = fixtures_full.awayteam_id)

JOIN
(SELECT hometeam_id,
        awayteam_id,
        avg(awaycorners) AS hth_ca,
        avg(awayfouls) AS hth_fa,
        avg(awaygoals) AS hth_ga,
        avg(awaygoalsallowed) AS hth_gaa,
        avg(awayredcards) AS hth_ra,
        avg(awayshots) AS hth_sa,
        avg(awayshotsontarget) AS hth_sota,
        avg(awayyellowcards) AS hth_ya,
        avg(halftimeawaygoals) AS hth_htga,
        avg(homecorners) AS hth_ch,
        avg(homefouls) AS hth_fh,
        avg(homegoals) AS hth_gh,
        avg(homegoalsallowed) AS hth_gah,
        avg(homeredcards) AS hth_rh,
        avg(homeshots) AS hth_sh,
        avg(homeshotsontarget) AS hth_soth,
        avg(homeyellowcards) AS hth_yh,
        avg(halftimehomegoals) AS hth_htgh
FROM fixtures_full
GROUP BY hometeam_id, awayteam_id) AS hth
ON hth.hometeam_id = fixtures_full.hometeam_id AND hth.awayteam_id = fixtures_full.awayteam_id;
