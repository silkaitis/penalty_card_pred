Script workflow

1. Initial collection of English Premier League (EPL) data
  1. **epl_extract.py** - Save match data from the XML API into json files
    * Uses extract_data_funcs.py to operate
    * Waits the appropriate time between requests (1 hour)
  2. **referee_scrape.py** - Scrape worldfootball.net for referee performance and save into MongoDB
2. Build SQL databases
  1. **fixtures_to_sql.py** - Move JSON match data into postgresql
  2. **xml_to_epl.py** - Create SQL table and dictionary of team_id and team name for later use
  3. **worldfootball_to_epl.py** - Create dictionary for team_id and team name that standardizes name to official EPL titles
  4. **referee_list.py** - Create SQL table of all referees in the EPL from 2000 to 2016
  5. **ref_details_sql.py** - Move MongoDB referee data into postgresql
  6. **trans_fixtures.py** - Transpose fixture data and create new SQL table
3. Prepare data for modeling
  1. **prep_model_data.py** - Build analytical base table (ABT)
    * rolling_team_status.py - Calculate a moving sum of team performance
    * historical_query.py - Calculate performance averages per team based on team history
    * rolling_ref_status.py - Calculate a moving sum of referee performance (Needs to be created, may want to roll into other scripts)
    * historical_ref_query.py - Calculate performance averages per referee based on history (Needs to be created, may want to roll into other scripts)
4. Build Model
  1. **build_model.py** - Transform ABT, pass into model(s), evaluate model performance and save model pickle
    * feature_eng.py - Transforms ABT into model features
5. Predict Match
  1. **pred_match.py** - Based on an away and home team, create a fictitious match to have the model predict
    * feature_eng.py - Transforms fake match ABT into model features
6. Update Data
  1. **season_update.py** - Updates JSON files and MongoDB with latest EPL matches

After the model is built, pred_match.py is the only script needed to make predictions. Steps 3 and 4 must be re-run after season data is updated (step 6).

Note: Scripts only in bold need to be executed to rebuild the project.
