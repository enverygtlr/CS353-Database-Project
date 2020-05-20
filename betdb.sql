CREATE SCHEMA public;
CREATE TABLE SUSER (
   id smallserial PRIMARY KEY,
   s_name VARCHAR(25) NOT NULL UNIQUE,
   s_password VARCHAR(255) NOT NULL,
   email VARCHAR(255) NOT NULL,
   s_type VARCHAR(255) NOT NULL
);
 
CREATE TABLE Admin(
   id     smallint PRIMARY KEY,
   salary numeric(6,2) NOT NULL,
   FOREIGN KEY(id) REFERENCES SUSER(id)
);
 
CREATE TABLE Player (
   id     smallint PRIMARY KEY,
   balance numeric(10,2) NOT NULL,
   no_of_followers smallint NOT NULL,
   FOREIGN KEY(id) REFERENCES SUSER(id) 
);
 
CREATE TABLE Editor(
   id     smallint PRIMARY KEY,
   salary numeric(6, 2) NOT NULL,
   success_rate numeric(3,2) NOT NULL,
   successful_bets smallint NOT NULL,
   total_bets smallint NOT NULL,
   no_of_followers smallint NOT NULL,
   FOREIGN KEY(id) REFERENCES SUSER(id)
); 
CREATE TABLE Match (
           match_id        smallserial PRIMARY KEY,
           home_team_id        smallint NOT NULL,
           away_team_id        smallint NOT NULL,
           league_id           smallint NOT NULL,
           match_date        TIMESTAMP NOT NULL,
           home_score        INT NOT NULL,
           away_score        INT NOT NULL,
           FOREIGN KEY(home_team_id) REFERENCES Team(team_id),
           FOREIGN KEY(league_id) REFERENCES League(league_id),
           FOREIGN KEY(away_team_id) REFERENCES Team(team_id));

CREATE TABLE Bet (
    bet_id smallserial PRIMARY KEY,
    mbn smallint NOT NULL,
    bet_type VARCHAR(30),
    cancelled smallint NOT NULL,
    match_id smallserial REFERENCES Match(match_id)
);



CREATE TABLE Betslip (
           betslip_id        smallserial PRIMARY KEY,
           creator_user_id   smallint NOT NULL REFERENCES SUSER(id),
           stake             NUMERIC(10,2) NOT NULL,
           shared            INT NOT NULL,
           betslip_date      TIMESTAMP NOT NULL,
           total_odd         NUMERIC(6,3) NOT NULL);
CREATE TABLE SportBranch (
           branch_name         VARCHAR(30) PRIMARY KEY);
CREATE TABLE League (
           league_id          smallserial PRIMARY KEY NOT NULL,
           branch_name        VARCHAR(30) NOT NULL,
           league_name        VARCHAR(30) NOT NULL,
           no_of_teams        INT NOT NULL,
           FOREIGN KEY(branch_name) REFERENCES SportBranch(branch_name));
CREATE TABLE Team (
            team_id        smallserial PRIMARY KEY,
           league_id        smallint NOT NULL,
           name            VARCHAR(30) NOT NULL,
           standing        INT NOT NULL,
           point            INT NOT NULL,
           FOREIGN KEY(league_id) REFERENCES League(league_id));

CREATE TABLE Bet (
           bet_id        smallserial PRIMARY KEY,
           match_id    smallint NOT NULL,
           mbn        INT NOT NULL,
           bet_type    VARCHAR(30),
           cancelled    INT NOT NULL,
           FOREIGN KEY(match_id) REFERENCES Match(match_id));
CREATE TABLE Odd(
           odd        NUMERIC(5, 2) NOT NULL,
           odd_timestamp      TIMESTAMP NOT NULL,
           bet_id         smallint NOT NULL,
           FOREIGN KEY(bet_id) REFERENCES Bet(bet_id));
CREATE TABLE Post (
              post_id                smallserial PRIMARY KEY,
              no_of_people_played    INT NOT NULL,
              betslip_id            smallint,
              user_id            smallint,
              no_of_likes        INT,
              post_date            TIMESTAMP,
              FOREIGN KEY(betslip_id) REFERENCES Betslip(betslip_id),
              FOREIGN KEY(user_id) REFERENCES SUSER(id));
CREATE TABLE Comment(
           comment_id        smallserial PRIMARY KEY,
           post_id           smallint NOT NULL,
           context            VARCHAR(2048),
           FOREIGN KEY(post_id) REFERENCES Post(post_id));
CREATE TABLE Transaction (
           transaction_id         smallserial PRIMARY KEY,
           transaction_type               VARCHAR(10) NOT NULL,
       transaction_date            date NOT NULL,
       amount        NUMERIC(10,2) NOT NULL,
       receiver_player_id    smallint NOT NULL,
       sender_player_id    smallint NOT NULL,
           FOREIGN KEY(receiver_player_id) REFERENCES SUSER(id),
       FOREIGN KEY(sender_player_id) REFERENCES SUSER(id));
CREATE TABLE Contract(
           transaction_id        smallint PRIMARY KEY,
           odd            NUMERIC(3,2) NOT NULL,
           agreed            BOOL NOT NULL,
           completed         BOOL NOT NULL,
           result             BOOL NOT NULL,
           ratio             BOOL NOT NULL,
           FOREIGN KEY(transaction_id) REFERENCES Transaction(transaction_id));
CREATE TABLE UserFollows (
           follower_id        smallint,
           followee_id        smallint,
           FOREIGN KEY(follower_id) REFERENCES SUSER(id),
           FOREIGN KEY(followee_id) REFERENCES SUSER(id),
       PRIMARY KEY (follower_id, followee_id));
CREATE TABLE Editor_Suggests(
           bet_id       smallint,
           user_id        smallint,
           trust        INT,
           shared_content         VARCHAR(30),
           FOREIGN KEY(bet_id) REFERENCES Bet(bet_id),
           FOREIGN KEY(user_id) REFERENCES SUSER(id),
       PRIMARY KEY(bet_id, user_id));
CREATE TABLE BetSlipHas(
           betslip_id        smallint NOT NULL,
           bet_id            smallint NOT NULL,
           FOREIGN KEY(betslip_id) REFERENCES Betslip(betslip_id),
           FOREIGN KEY(bet_id) REFERENCES Bet(bet_id),
       PRIMARY KEY (betslip_id, bet_id));

CREATE TABLE PostLikes(
           post_id          smallint NOT NULL,
           user_id          smallint NOT NULL,
           FOREIGN KEY(post_id) REFERENCES Post(post_id),
           FOREIGN KEY(user_id) REFERENCES SUSER(id),
           PRIMARY KEY(post_id, user_id));
create view currentBetView as
with current_odd as
(
   select O2.odd, O2.odd_timestamp, O2.bet_id
   from (select bet_id,max(odd_timestamp) from odd group by bet_id) as O1, odd as O2 
   where O2.bet_id = O1.bet_id and O2.odd_timestamp = O1.max
)
select bet_id, match_id, branch_name, league_name, match_date, home_score, away_score, mbn, bet_type, cancelled, odd, odd_timestamp,
t1.name as t1name, t2.name as t2name
from sportbranch natural join league natural join match natural join bet natural join current_odd, team as t1, team as t2
where t1.team_id = home_team_id and t2.team_id = away_team_id
order by match_date desc;