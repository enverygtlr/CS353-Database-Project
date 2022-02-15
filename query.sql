/* filter bets with given :'date' :'league' :'bet_type'
   return: filtered match + bet records.
*/ 
with league_matches as 
(
    select * from match, team, league where home_team_id = team_id;
)

f'''
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
    '''
