## Business Understanding

  A yellow and red card is used during soccer matches as a means of warning, reprimanding or penalizing a player, coach or team official. Each card has a different consequence for the player that received it. A single yellow card is a warning while two yellow cards means the player is ejected the match. Additionally, yellow card accumulation across matches has consequences as well, usually disqualification from the next match. A red card is an immediate ejection from the match. A player cannot be replaced by a substitute if the player was ejected from the match. Also, the ejected player may be disqualified from the next match or more.

  Penalty card consequences can impact team performance through key players being unavailable for a match. Predicting whether cards will be issued or not could offer coaching staff a competitive advantage. Card prediction could be used in setting odds for bets on matches outcomes. There are multiple levels to the prediction model that can be implemented.
  1. Predict how many penalty cards per match will be issued and to which team
  2. Predict which player will receive a penalty card and which one
  3. Predict when a player will receive a penalty card

## Data Understanding

[English Premier League](https://www.premierleague.com/) (EPL) was selected for the analysis due to the popularity of the league and data availability. [XMLsoccer](http://xmlsoccer.com/) has EPL match and league data starting at the '00/'01 season to the current season. XMLsoccer offers traditional match statistics from number of goals, fouls, penalty cards, etc. The official EPL website can easily be scraped for additional information that may not be included in the XMLsoccer API. Portions of the site are dynamic requiring selenium to reach the desired HTML content. Otherwise, simple web scraping can extract the desired information. Below are the additional types of data on the league:
* [Head-to-head](https://www.premierleague.com/stats/head-to-head) team statistics
* In-depth [club and player](https://www.premierleague.com/clubs/12/Manchester-United/stats) statistics

Internet searches reveal even more information currently found through XMLsoccer and EPL official site.
* [Referee](http://www.worldfootball.net/referees/eng-premier-league-2000-2001/1/) statistics per season
* [Attendance](http://www.worldfootball.net/attendance/eng-premier-league-2000-2001/1/) per season and team
* [Team wages](https://docs.google.com/spreadsheets/d/1TA-8JcPKP9J4uSIv_yQY9olClw5X5J2yoy7OEjtgqX8/edit#gid=0) per season

## Data Preparation

Raw data will need to be consolidated into a single database to enable feature engineering. A combination of technologies will be needed to effectively consolidate. PostgreSQL and MongoDB are the primary candidates for the storage and consolidation effort. MongoDB will house any raw HTML scraped from websites while PostgreSQL will function as a database. The output is an analytical base table that feature engineering can be conducted on.

Feature engineering will be an important to develop meaningful relationships between teams and penalty cards. Features for team-level predictions may be different than those needed for player-level predictions. Therefore, team-level predictions will be the initial focus for feature engineering before moving onto the next phase. Preliminary features for team-level predictions are listed below:

  * Average ____ per team over the last 3 matches
    * Cards, fouls, points, goals for and against, clean sheets, attendance,  
  * Average ____ per match per team for an entire season
    * Cards, fouls, points, goals for and against, clean sheets, attendance,
  * Average head-to-head ____
    * Cards, fouls, points, goals for and against, clean sheets,
  * Average cards and fouls per referee over the last 3 matches
  * Average cards and fouls per referee for an entire season
  * Match referee
  * Rivalry status
  * Relegation status
  * Average cards received by each referee per team
  * Number of days since last match
  * Number of matches since last yellow card
  * Number of matches since last red card
  * Match week
  * Match day of week

## Modeling

Multioutput regression was used to predict match outcomes to eliminate the need to encode match outcomes. Most Sklearn models can be used for multioutput prediction either natively or through the [multioutput](http://scikit-learn.org/stable/modules/classes.html#module-sklearn.multioutput) module. Model classes listed below are being considered.

  1. Linear Regression
  2. Lasso Regression
  3. Ensemble Methods
    * Gradient Boosting
    * Random Forest Regressors

## Evaluation

Cross validation and bootstrap sampling was used to assess all models investigated against a baseline model. The baseline model used the average penalty cards for a team given the opposing team. Mean squared error will be used to evaluate the performance of each model against a baseline.

Linear regression was selected for the final model for simplicity and similar performance to more complicated models. Graph below illustrates model performance against the baseline for home team yellow cards.

![Model Comparison](https://github.com/silkaitis/penalty_card_pred/blob/master/img/Model%20Comparison.png?raw=true)

## Deployment

Most matches occur on Saturday or Sunday in the English Premier League. Predictions can be made through a web application located at [www.danius.tech](http://www.danius.tech) at any time. The base analytical table will be updated at beginning of each week to incorporate the latest match results.

The initial app version will only predict number of penalty cards for a given team; not players on a particular team.
