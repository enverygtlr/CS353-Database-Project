insert into SportBranch(branch_name)
values ('football');

insert into League(league_id, branch_name, league_name, no_of_teams)
values(DEFAULT,'football','superlig',20);

insert into League(league_id, branch_name, league_name, no_of_teams)
values(DEFAULT,'football','bankasya',14);



insert into Team(league_id, name, standing, point)
values((select league_id from League where league_name = 'superlig'),'fenerbahce',10,9);

insert into Team(league_id, name, standing, point)
values((select league_id from League where league_name = 'superlig'),'galatasaray',4,6);

insert into Team(league_id, name, standing, point)
values((select league_id from League where league_name = 'superlig'),'trabzon',5,5);

insert into Team(league_id, name, standing, point)
values((select league_id from League where league_name = 'superlig'),'besiktas',4,14);

insert into Team(league_id, name, standing, point)
values((select league_id from League where league_name = 'superlig'),'bursa',4,6);

insert into Team(league_id, name, standing, point)
values((select league_id from League where league_name = 'bankasya'),'goztepe',10,9);

insert into Team(league_id, name, standing, point)
values((select league_id from League where league_name = 'bankasya'),'altay',4,6);

insert into Team(league_id, name, standing, point)
values((select league_id from League where league_name = 'bankasya'),'karsiyaka',5,5);

insert into Team(league_id, name, standing, point)
values((select league_id from League where league_name = 'bankasya'),'osmanlispor',4,14);

insert into Team(league_id, name, standing, point)
values((select league_id from League where league_name = 'bankasya'),'altinordu',4,6);




insert into Match(home_team_id, away_team_id, league_id, match_date, home_score, away_score)
values(
    (select team_id from Team where name = 'fenerbahce'),
    (select team_id from Team where name = 'bursa'),
    (select league_id from League where league_name = 'superlig'),
    '2019-02-19',
    0,0
);

insert into Bet(match_id, mbn, bet_type, cancelled)
values(
    (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'fenerbahce' and t2.name = 'bursa' and home_team_id = t1.team_id and away_team_id = t2.team_id),
    5,
    '1.5 ALT',
    0
);

insert into Odd(odd, odd_timestamp , bet_id)
values(
    4.52,
    '2019-03-12 22:01:25',
    (select bet_id from Bet where match_id = (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'fenerbahce' and t2.name = 'bursa' and home_team_id = t1.team_id and away_team_id = t2.team_id) and bet_type = '1.5 ALT')
);

insert into Bet(match_id, mbn, bet_type, cancelled)
values(
    (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'fenerbahce' and t2.name = 'bursa' and home_team_id = t1.team_id and away_team_id = t2.team_id),
    5,
    'MS X',
    0
);

insert into Odd(odd, odd_timestamp , bet_id)
values(
    4.52,
    '2019-03-12 22:01:25',
    (select bet_id from Bet where match_id = (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'fenerbahce' and t2.name = 'bursa' and home_team_id = t1.team_id and away_team_id = t2.team_id) and bet_type = 'MS X')
);


insert into Match(home_team_id, away_team_id, league_id, match_date, home_score, away_score)
values(
    (select team_id from Team where name = 'galatasaray'),
    (select team_id from Team where name = 'bursa'),
    (select league_id from League where league_name = 'superlig'),
    '2019-02-19',
    0,0
);

insert into Bet(match_id, mbn, bet_type, cancelled)
values(
    (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'galatasaray' and t2.name = 'bursa' and home_team_id = t1.team_id and away_team_id = t2.team_id),
    5,
    'MS 1',
    0
);

insert into Odd(odd, odd_timestamp , bet_id)
values(
    4.52,
    '2019-03-12 22:01:25',
    (select bet_id from Bet where match_id = (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'galatasaray' and t2.name = 'bursa' and home_team_id = t1.team_id and away_team_id = t2.team_id) and bet_type = 'MS 1')
);

insert into Bet(match_id, mbn, bet_type, cancelled)
values(
    (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'galatasaray' and t2.name = 'bursa' and home_team_id = t1.team_id and away_team_id = t2.team_id),
    5,
    'MS X',
    0
);

insert into Odd(odd, odd_timestamp , bet_id)
values(
    1.02,
    '2019-03-12 22:01:25',
    (select bet_id from Bet where match_id = (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'galatasaray' and t2.name = 'bursa' and home_team_id = t1.team_id and away_team_id = t2.team_id) and bet_type = 'MS X')
);

insert into Bet(match_id, mbn, bet_type, cancelled)
values(
    (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'galatasaray' and t2.name = 'bursa' and home_team_id = t1.team_id and away_team_id = t2.team_id),
    12,
    '2.5 UST',
    0
);

insert into Odd(odd, odd_timestamp , bet_id)
values(
    3.31,
    '2019-03-12 22:01:25',
    (select bet_id from Bet where match_id = (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'galatasaray' and t2.name = 'bursa' and home_team_id = t1.team_id and away_team_id = t2.team_id) and bet_type = '2.5 UST')
);



insert into Match(home_team_id, away_team_id, league_id, match_date, home_score, away_score)
values(
    (select team_id from Team where name = 'trabzon'),
    (select team_id from Team where name = 'besiktas'),
    (select league_id from League where league_name = 'superlig'),
    '2019-02-19',
    0,0
);

insert into Bet(match_id, mbn, bet_type, cancelled)
values(
    (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'trabzon' and t2.name = 'besiktas' and home_team_id = t1.team_id and away_team_id = t2.team_id),
    5,
    'MS 2',
    0
);

insert into Odd(odd, odd_timestamp , bet_id)
values(
    1.52,
    '2019-03-12 22:01:25',
    (select bet_id from Bet where match_id = (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'trabzon' and t2.name = 'besiktas' and home_team_id = t1.team_id and away_team_id = t2.team_id) and bet_type = 'MS 2')
);

insert into Bet(match_id, mbn, bet_type, cancelled)
values(
    (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'trabzon' and t2.name = 'besiktas' and home_team_id = t1.team_id and away_team_id = t2.team_id),
    5,
    'ALT',
    0
);

insert into Odd(odd, odd_timestamp , bet_id)
values(
    0.01,
    '2019-03-12 22:01:25',
    (select bet_id from Bet where match_id = (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'trabzon' and t2.name = 'besiktas' and home_team_id = t1.team_id and away_team_id = t2.team_id) and bet_type = 'ALT')
);

insert into Odd(odd, odd_timestamp , bet_id)
values(
    0.01,
    '2020-03-12 23:01:25',
    (select bet_id from Bet where match_id = (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'trabzon' and t2.name = 'besiktas' and home_team_id = t1.team_id and away_team_id = t2.team_id) and bet_type = 'ALT')
);


insert into Match(home_team_id, away_team_id, league_id, match_date, home_score, away_score)
values(
    (select team_id from Team where name = 'trabzon'),
    (select team_id from Team where name = 'fenerbahce'),
    (select league_id from League where league_name = 'superlig'),
    '2019-02-19',
    0,0
);

insert into Bet(match_id, mbn, bet_type, cancelled)
values(
    (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'trabzon' and t2.name = 'fenerbahce' and home_team_id = t1.team_id and away_team_id = t2.team_id),
    5,
    '2.5 ALT',
    0
);

insert into Odd(odd, odd_timestamp , bet_id)
values(
    4.52,
    '2020-03-11 22:10:25',
    (select bet_id from Bet where match_id = (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'trabzon' and t2.name = 'fenerbahce' and home_team_id = t1.team_id and away_team_id = t2.team_id) and bet_type = '2.5 ALT')
);

insert into Match(home_team_id, away_team_id, league_id, match_date, home_score, away_score)
values(
    (select team_id from Team where name = 'galatasaray'),
    (select team_id from Team where name = 'fenerbahce'),
    (select league_id from League where league_name = 'superlig'),
    '2020-02-19',
    0,0
);

insert into Bet(match_id, mbn, bet_type, cancelled)
values(
    (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'galatasaray' and t2.name = 'fenerbahce' and home_team_id = t1.team_id and away_team_id = t2.team_id),
    5,
    'MS X',
    0
);

insert into Odd(odd, odd_timestamp , bet_id)
values(
    11.52,
    '2020-03-11 22:10:25',
    (select bet_id from Bet where match_id = (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'galatasaray' and t2.name = 'fenerbahce' and home_team_id = t1.team_id and away_team_id = t2.team_id) and bet_type = 'MS X')
);

insert into Bet(match_id, mbn, bet_type, cancelled)
values(
    (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'galatasaray' and t2.name = 'fenerbahce' and home_team_id = t1.team_id and away_team_id = t2.team_id),
    3,
    'MS 1',
    0
);

insert into Odd(odd, odd_timestamp , bet_id)
values(
    13.52,
    '2020-03-11 22:11:25',
    (select bet_id from Bet where match_id = (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'galatasaray' and t2.name = 'fenerbahce' and home_team_id = t1.team_id and away_team_id = t2.team_id) and bet_type = 'MS 1')
);


insert into Bet(match_id, mbn, bet_type, cancelled)
values(
    (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'galatasaray' and t2.name = 'fenerbahce' and home_team_id = t1.team_id and away_team_id = t2.team_id),
    3,
    'MS 2',
    0
);

insert into Odd(odd, odd_timestamp , bet_id)
values(
    3.50,
    '2020-03-11 22:11:25',
    (select bet_id from Bet where match_id = (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'galatasaray' and t2.name = 'fenerbahce' and home_team_id = t1.team_id and away_team_id = t2.team_id) and bet_type = 'MS 2')
);


insert into Match(home_team_id, away_team_id, league_id, match_date, home_score, away_score)
values(
    (select team_id from Team where name = 'goztepe'),
    (select team_id from Team where name = 'altay'),
    (select league_id from League where league_name = 'bankasya'),
    '2020-02-19',
    0,0
);

insert into Bet(match_id, mbn, bet_type, cancelled)
values(
    (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'goztepe' and t2.name = 'altay' and home_team_id = t1.team_id and away_team_id = t2.team_id),
    5,
    'MS X',
    0
);

insert into Odd(odd, odd_timestamp , bet_id)
values(
    1.52,
    '2020-03-11 22:10:25',
    (select bet_id from Bet where match_id = (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'goztepe' and t2.name = 'altay' and home_team_id = t1.team_id and away_team_id = t2.team_id) and bet_type = 'MS X')
);

insert into Match(home_team_id, away_team_id, league_id, match_date, home_score, away_score)
values(
    (select team_id from Team where name = 'altinordu'),
    (select team_id from Team where name = 'karsiyaka'),
    (select league_id from League where league_name = 'bankasya'),
    '2020-02-19',
    0,0
);

insert into Bet(match_id, mbn, bet_type, cancelled)
values(
    (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'altinordu' and t2.name = 'karsiyaka' and home_team_id = t1.team_id and away_team_id = t2.team_id),
    5,
    '1.5 UST',
    0
);

insert into Odd(odd, odd_timestamp , bet_id)
values(
    9.82,
    '2020-03-11 22:10:25',
    (select bet_id from Bet where match_id = (select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'altinordu' and t2.name = 'karsiyaka' and home_team_id = t1.team_id and away_team_id = t2.team_id) and bet_type = '1.5 UST')
);

insert into suser(id, s_name, s_password, email, s_type)
values(DEFAULT, 'ahmet2' ,'muzafsert' ,'ahmet2@email' ,'player');
insert into player(id, balance, no_of_followers)
values((select id from suser where s_name = 'ahmet2'), 130.0, 0);

insert into suser(id, s_name, s_password, email, s_type)
values(DEFAULT, 'ahmet3' ,'muzafsert' ,'ahmet3@email' ,'player');
insert into player(id, balance, no_of_followers)
values((select id from suser where s_name = 'ahmet3'), 13.0, 0);

insert into suser(id, s_name, s_password, email, s_type)
values(DEFAULT, 'ahmet4' ,'muzafsert' ,'ahmet4@email' ,'player');
insert into player(id, balance, no_of_followers)
values((select id from suser where s_name = 'ahmet4'), 12.5, 0);

insert into suser(id, s_name, s_password, email, s_type)
values(DEFAULT, 'ahmet5' ,'muzafsert' ,'ahmet5@email' ,'player');
insert into player(id, balance, no_of_followers)
values((select id from suser where s_name = 'ahmet5'), 102.0, 0);

insert into suser(id, s_name, s_password, email, s_type)
values(DEFAULT, 'ahmet6' ,'muzafsert' ,'ahmet6@email' ,'player');
insert into player(id, balance, no_of_followers)
values((select id from suser where s_name = 'ahmet6'), 680.0, 0);

insert into suser(id, s_name, s_password, email, s_type)
values(DEFAULT, 'admin1' ,'muzafsert' ,'admin1@email' ,'admin');
insert into admin(id, salary)
values((select id from suser where s_name = 'admin1'), 1500.0);

insert into suser(id, s_name, s_password, email, s_type)
values(DEFAULT, 'admin2' ,'muzafsert' ,'admin2@email' ,'admin');
insert into admin(id, salary)
values((select id from suser where s_name = 'admin2'), 2000.0);

insert into suser(id, s_name, s_password, email, s_type)
values(DEFAULT, 'admin3' ,'muzafsert' ,'admin3@email' ,'admin');
insert into admin(id, salary)
values((select id from suser where s_name = 'admin3'), 3000.0);

insert into suser(id, s_name, s_password, email, s_type)
values(DEFAULT, 'admin4' ,'muzafsert' ,'admin4@email' ,'admin');
insert into admin(id, salary)
values((select id from suser where s_name = 'admin4'), 4000.0);

insert into suser(id, s_name, s_password, email, s_type)
values(DEFAULT, 'editor1' ,'muzafsert' ,'editor@email' ,'editor');
insert into editor(id, salary, success_rate, successful_bets, total_bets, no_of_followers)
values((select id from suser where s_name = 'editor1'), 4000.0, 0, 0,0,0);
  


insert into BetSlip(betslip_id, creator_user_id, stake, shared, betslip_date,total_odd) 
values(DEFAULT, (select id from suser where s_name = 'ahmet2'),10, 1,'1999-02-21 10:32:23',1 );

insert into BetSlipHas(betslip_id, bet_id)
values( (select betslip_id from BetSlip,Suser where creator_user_id = id and s_name = 'ahmet2') 
 , (select bet_id from (Bet natural join Match) where bet_type = '1.5 UST' and match_id =(select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'altinordu' and t2.name = 'karsiyaka' and home_team_id = t1.team_id and away_team_id = t2.team_id)));

insert into BetSlipHas(betslip_id, bet_id)
values( (select betslip_id from BetSlip,Suser where creator_user_id = id and s_name = 'ahmet2' and betslip_date = '1999-02-21 10:32:23') 
 , (select bet_id from (Bet natural join Match) where bet_type = 'MS X' and match_id =(select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'goztepe' and t2.name = 'altay' and home_team_id = t1.team_id and away_team_id = t2.team_id)));



insert into BetSlip(betslip_id, creator_user_id, stake, shared, betslip_date,total_odd) 
values(DEFAULT, (select id from suser where s_name = 'ahmet3'),150.50, 1,'2020-02-21 11:32:23' , 1);

insert into BetSlipHas(betslip_id, bet_id)
values( (select betslip_id from BetSlip,Suser where creator_user_id = id and s_name = 'ahmet3' and betslip_date = '2020-02-21 11:32:23') 
 , (select bet_id from (Bet natural join Match) where bet_type = 'MS 2' and match_id =(select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'galatasaray' and t2.name = 'fenerbahce' and home_team_id = t1.team_id and away_team_id = t2.team_id)));

insert into BetSlip(betslip_id, creator_user_id, stake, shared, betslip_date ,total_odd) 
values(DEFAULT, (select id from suser where s_name = 'ahmet4'),150.50, 1,'2018-03-11 12:42:23' , 1);

insert into BetSlipHas(betslip_id, bet_id)
values( (select betslip_id from BetSlip,Suser where creator_user_id = id and s_name = 'ahmet4' and betslip_date = '2018-03-11 12:42:23') 
 , (select bet_id from (Bet natural join Match) where bet_type = 'MS 2' and match_id =(select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'galatasaray' and t2.name = 'fenerbahce' and home_team_id = t1.team_id and away_team_id = t2.team_id)));


/*  Post, Comment, user_follows, post_like */
    
insert into Post(no_of_people_played, betslip_id, user_id, no_of_likes, post_date)
values(0, 
(select betslip_id from BetSlip,Suser where creator_user_id = id and s_name = 'ahmet4' and betslip_date = '2018-03-11 12:42:23'),
(select id from suser where s_name = 'ahmet4'), 0, '2018-12-01 10:15:16');

    
insert into Post(no_of_people_played, betslip_id, user_id, no_of_likes, post_date)
values(0, 
(select betslip_id from BetSlip,Suser where creator_user_id = id and s_name = 'ahmet3' and betslip_date =  '2020-02-21 11:32:23'),
(select id from suser where s_name = 'ahmet3'), 0, '2017-12-01 12:15:13');

    
insert into Post(no_of_people_played, betslip_id, user_id, no_of_likes, post_date)
values(0, 
(select betslip_id from BetSlip,Suser where creator_user_id = id and s_name = 'ahmet2' and betslip_date = '1999-02-21 10:32:23'),
(select id from suser where s_name = 'ahmet2'), 0, '2017-11-02 13:13:31');


/*comment*/
insert into Comment(post_id, context)
values((select post_id from Post, Suser where user_id = id and s_name = 'ahmet2' and post_date = '2017-11-02 13:13:31'),
'This is a comment');

insert into Comment(post_id, context)
values((select post_id from Post, Suser where user_id = id and s_name = 'ahmet3' and post_date = '2017-12-01 12:15:13'),
'This is an another comment');


/*user follows*/
insert into UserFollows(follower_id, followee_id)
values((select id from suser where s_name = 'ahmet4'),(select id from suser where s_name = 'ahmet3'));

insert into UserFollows(follower_id, followee_id)
values((select id from suser where s_name = 'ahmet2'),(select id from suser where s_name = 'ahmet4'));

insert into UserFollows(follower_id, followee_id)
values((select id from suser where s_name = 'admin1'),(select id from suser where s_name = 'ahmet3'));

insert into UserFollows(follower_id, followee_id)
values((select id from suser where s_name = 'admin2'),(select id from suser where s_name = 'ahmet3'));

/*postlike*/

insert into PostLikes(post_id, user_id)
values((select post_id from Post, Suser where user_id = id and s_name = 'ahmet2' and post_date = '2017-11-02 13:13:31'),
(select id from suser where s_name = 'admin1'));

insert into PostLikes(post_id, user_id)
values((select post_id from Post, Suser where user_id = id and s_name = 'ahmet2' and post_date = '2017-11-02 13:13:31'),
(select id from suser where s_name = 'admin2'));

/*editor suggests*/
insert into Editor_Suggests(bet_id, user_id, trust, shared_content)
values((select bet_id from (Bet natural join Match) where bet_type = 'MS 2' and match_id =(select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'galatasaray' and t2.name = 'fenerbahce' and home_team_id = t1.team_id and away_team_id = t2.team_id)),
   (select id from suser where s_name = 'editor1'),
   10,
   'banko bet');

insert into Editor_Suggests(bet_id, user_id, trust, shared_content)
values((select bet_id from (Bet natural join Match) where bet_type = '1.5 UST' and match_id =(select match_id from Match , Team as t1, Team as t2 
    where t1.name = 'altinordu' and t2.name = 'karsiyaka' and home_team_id = t1.team_id and away_team_id = t2.team_id)) ,
   (select id from suser where s_name = 'editor1'),
   10,
   'oynayin');


