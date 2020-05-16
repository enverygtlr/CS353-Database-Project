DROP TABLE IF EXISTS SUSER CASCADE;


CREATE TABLE SUSER (
    id smallserial PRIMARY KEY,
    s_name VARCHAR(25) NOT NULL UNIQUE,
    s_password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    s_type VARCHAR(255) NOT NULL
);

CREATE TABLE Admin(
    salary numeric(6,2) NOT NULL
) INHERITS(SUSER);

CREATE TABLE Player (
    balance numeric(10,2) NOT NULL,
    no_followers smallint NOT NULL
) INHERITS(SUSER);

CREATE TABLE Editor(
    salary numeric(6, 2) NOT NULL,
    success_rate numeric(3,2) NOT NULL,
    successful_bets smallint NOT NULL,
    total_bets smallint NOT NULL,
    no_of_followers smallint NOT NULL
   
)INHERITS (SUSER); 

/*
CREATE TABLE Bet (
    bet_id smallserial PRIMARY KEY,
    mbn smallint NOT NULL,
    bet_type VARCHAR(30),
    cancelled smallint NOT NULL,
    match_id smallserial REFERENCES Match(match_id)
);

CREATE TABLE Match (
    match_id smallserial PRIMARY KEY,
    home_team_id smallint NOT NULL,
    away_team_id smallint NOT NULL,
    match_date date NOT NULL,
    home_score smallint NOT NULL,
    away_score smallint NOT NULL
);

CREATE TABLE Odd(
    odd NUMERIC(3, 2) NOT NULL,
    date_suggested date NOT NULL,
    bet_id smallserial REFERENCES Bet(bet_id)
);

CREATE TABLE Team (
    team_id smallint PRIMARY KEY,
    league_id smallint NOT NULL,
    name varchar(30) NOT NULL,
    standing smallint NOT NULL,
    point smallint NOT NULL,
    league_id smallint REFERENCES League(league_id)
);

CREATE TABLE League (
    league_id smallserial PRIMARY KEY NOT NULL,
    branch_name varchar(30) NOT NULL,
    league_name varchar(30) NOT NULL,
    no_of_teams smallint NOT NULL,
    branch_name REFERENCES SportBranch(branch_name)
);*/