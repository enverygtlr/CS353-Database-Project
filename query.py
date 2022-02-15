import psycopg2
import psycopg2.extras
import sys

from datetime import date

print('your mom')

def connectToDB():
    connectionString = 'dbname=bet user=postgres password=postgres host=localhost'
    try:
        return psycopg2.connect(connectionString)
    except:
        print("cant connect to db")        


conn = connectToDB()
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def getBetTable(sportbranch = "-", league = "-" , minDate = "-"):
    #show all bets given branch, league, mindate
    where_clause = ''

    if sportbranch != '-':
        where_clause = where_clause + f' and branch_name = \'{sportbranch}\''
    
    if league != '-':
        where_clause = where_clause + f' and league_name = \'{league}\''
    
    if minDate != '-':
        where_clause = where_clause + f' and match_date > \'{minDate}\''
    
    currentBetTableRel = f'''
        select distinct match_id, branch_name, league_name,  match_date, home_score, away_score, t1name, t2name   
        from currentBetView
        where 1=1 {where_clause}
    '''

    try:
        cur.execute(currentBetTableRel)
    except:
        print("error running sql")
    
    matches = cur.fetchall()

  
    resultTable = []

    for match in matches:
        matchId = match["match_id"]

        getBetsQuery = f'''
            select mbn, bet_type, cancelled, odd, odd_timestamp 
            from currentBetView
            where match_id = {matchId} {where_clause}
        '''

        try:
            cur.execute(getBetsQuery)
        except:
            print("error running sql")
        
        
        bets = cur.fetchall()

        match['bets'] = bets

        resultTable.append(match)


    for row in resultTable:
        print(row)
        print(10*'\n')
   
    return resultTable

def findBetId(homeTeam, awayTeam, betType, matchDate):
    
    homeTeamIdQuery = f'''
        select team_id from Team where name = \'{homeTeam}\'
    '''
    print(homeTeamIdQuery)
    try:
        cur.execute(homeTeamIdQuery)
    except:
        print("error running sql")
    
    homeTeamId = cur.fetchall()[0][0]

    awayTeamIdQuery = f'''
        select team_id from Team where name = \'{awayTeam}\'
    ''' 
    
    try:
        cur.execute(awayTeamIdQuery)
    except:
        print("error running sql")
    
    awayTeamId = cur.fetchall()[0][0]
    print(awayTeamId) 
    matchIdQuery = f'''
        select match_id from match where home_team_id = {homeTeamId} and away_team_id = {awayTeamId} and match_date = \'{matchDate}\'
    '''

    print(matchIdQuery)
    try:
        cur.execute(matchIdQuery)
    except:
        print("error running sql")
    
    matchId = cur.fetchall()[0][0]

    betIdQuery = f'''
        select bet_id from bet where match_id = {matchId} and bet_type = \'{betType}\'
    '''
    try:
        cur.execute(betIdQuery)
    except:
        print("error running sql")
    
    betId = cur.fetchall()[0][0]

    return betId


def getAllBetSlipsOfUser(user_id):
    betSlipQuery = f'''
        select *
        from betslip, suser
        where creator_user_id = id and creator_user_id = {user_id}
    '''
    try:
        cur.execute(betSlipQuery)
    except:
        print("error running sql")

    betslipList = cur.fetchall()
    for row in betslipList:
        print(row)
    
    return betslipList


#admin queries
def cancelBet(homeTeam, awayTeam, betType, matchDate):
  
    betId = findBetId(homeTeam, awayTeam, betType, matchDate)
    
    timestampQuery = f'''
        select  max(odd_timestamp)
        from odd
        where bet_id = {betId}
        group by bet_id
    ''' 
    try:
        cur.execute(timestampQuery)
    except:
        print("error running sql")
    
    timeStamp = cur.fetchall()[0][0]

    print(timeStamp)

    cancelQuery = f'''
        update odd
        set cancelled = 1
        where bet_id = {betId} and odd_timestamp = \'{timeStamp}\'
    '''
    print(cancelQuery)
    try:
        cur.execute(cancelQuery)
        conn.commit()
    except:
        print("error running sql")


def update_odds(betId, newOdd):
    
    insertQuery = f'''
        insert into odd(odd, odd_timestamp, bet_id)
        values({newOdd}, \'{timestamp}\',{betId});
    '''
    print(insertQuery)
    try:
        cur.execute(insertQuery)
        conn.commit()
    except:
        print("error running sql")



def getBetsOfBetslip(betslip_id):
    betSelectQuery = f'''
        with oddofbet as 
        (select   bet_id, t1.name as t1name, t2.name as t2name , bet_type , mbn,  max(odd_timestamp) as odd_timestamp, match_date
        from betslip natural join betsliphas natural join bet natural join odd natural join match , team as t1 , team as t2 
        where betslip_id = {betslip_id} and home_team_id = t1.team_id  and away_team_id = t2.team_id and odd_timestamp < betslip_date
        group by  bet_id, t1name, t2name , mbn, bet_type, match_date)
        select * 
        from oddofbet natural join odd
    '''
    try:
        cur.execute(betSelectQuery)
    except:
        print("error running sql")
        
    betList = cur.fetchall()

    return betList


def get_user_betslips(user_id, include_private=False):
    sharedBet = ''
    if include_private == False:
        sharedBet = 'and shared = 1'

    betslipQuery = f'''
        select betslip_id, stake, total_odd, betslip_date
        from betslip
        where creator_user_id = {user_id} {sharedBet}
    '''
    try:
        cur.execute(betslipQuery)
    except:
        print("error running sql")

    betslipList = cur.fetchall()  
    
    print(betslipList)
    
    betslipIdQuery = f'''
        select betslip_id
        from betslip
        where creator_user_id = {user_id}
    '''
    try:
        cur.execute(betslipIdQuery)
    except:
        print("error running sql")

    betslipIdList= cur.fetchall()
    resultTable = []


    for betslip in betslipList:
        betslip['bet'] = getBetsOfBetslip(betslip['betslip_id'])
        resultTable.append(betslip)

    print(resultTable)
    return resultTable

def delete_user(user_id):
    query = f'''delete from suser where id = {user_id};'''

    try:
        cur.execute(query)
        conn.commit()
    except:
        print("error running sql")



#todo



def get_feed_posts(user_id):
    """ return format
       list = [
        {
            'betslip':
            {
                'expired':False,
                'betslip_id':0,
                'stake':1,
                'total_odd':3,
                'betslip_date':'May 3 2020',
                'bets':[
                    {
                        'team1':'FB', 
                        'team2':'BJK', 
                        'bet_type':'25ALT', 
                        'match_date':4, 
                        'mnbn':4, 
                        'odd':3.1
                    }
                ]
            },
            'username':'ali',
            'comments':[
                {'username':'ahmet',
                 'context' : 'Welldone blabamakjdnf'}
            ],
            'likes':23,
            'post_id':1
        }
    ] """
   
    query = f'''
        with followed_user_ids as 
        (select followee_id as followed_id, s_name
        from userfollows, suser
        where follower_id = {user_id}  and id = followee_id)
        select * from followed_user_ids,post where user_id = followed_id
    '''
    try:
        cur.execute(query)
    except:
        print("error running sql")

    postTable = cur.fetchall()

    resultTable = []
    
    for post in postTable:
        betslipQuery = f'''
            select betslip_id, stake, total_odd, betslip_date
            from betslip where betslip_id = {post['betslip_id']};
        '''
        try:
            cur.execute(betslipQuery)
        except:
            print("error running sql")  

        betslip = cur.fetchall()[0]
        betslip['bets'] = getBetsOfBetslip(post['betslip_id'])

        post['betslip'] = betslip

        commentQuery = f'''
            select s_name, context
            from (comment natural join post) , suser 
            where post_id = {post['post_id']} and id = commenter_id;
        '''
        try:
            cur.execute(commentQuery)
        except:
            print("error running sql")       
        
        post['comment'] = cur.fetchall()

        resultTable.append(post)
    
    for post in resultTable:
        print(post)
        print(10*'\n')

    return resultTable


def get_suggestions_by_editor(editor_id):
    query = f'''
        with live_odd as (
            select *
            from (select bet_id, max(odd_timestamp) as odd_timestamp from odd group by bet_id) as o1 natural join odd
         ),
         editor_info as (
             select  bet_id, user_id, trust, shared_content, s_name,  email 
             from editor_suggests, suser
             where user_id = {editor_id} and user_id = id
         )
        select  s_name , bet_id, user_id, trust,  shared_content, match_id , mbn , bet_type ,  odd_timestamp ,odd ,cancelled, t1.name as t1name, t2.name as t2name 
        from  editor_info natural join bet natural join live_odd natural join match, team as t1, team as t2
        where user_id = 10 and home_team_id = t1.team_id and away_team_id = t2.team_id; 
    '''
    suggestionList = execute(query, conn, select=True)
    
    print(suggestionList)
    return suggestionList


def get_suggestions_by_user(user_id):

    query = f'''
        with followed_user_ids as 
        (select followee_id as followed_id, s_name
        from userfollows, suser 
        where follower_id = {user_id} and id = followee_id),
        live_odd as (
            select *
            from (select bet_id, max(odd_timestamp) as odd_timestamp from odd group by bet_id) as o1 natural join odd
         )
        select  s_name , bet_id, user_id, trust,  shared_content, match_id , mbn , bet_type ,  odd_timestamp ,odd ,cancelled 
        from followed_user_ids, editor_suggests natural join bet natural join live_odd where user_id = followed_id;
    '''

    try:
        cur.execute(query)
    except:
        print("error running sql")       

    suggestionList = cur.fetchall()

    for suggestion in suggestionList:
        matchId = suggestion['match_id']

        teamQuery = f'''
            select t1.name as t1name, t2.name as t2name
            from match, team as t1, team as t2
            where match_id = {matchId} and home_team_id = t1.team_id and away_team_id = t2.team_id
        '''

        try:
            cur.execute(teamQuery)
        except:
            print("error running sql")
        
        teams = cur.fetchall()[0]

        suggestion['team1'] = teams['t1name']
        suggestion['team2'] = teams['t2name']

    
    print(suggestionList)
    return suggestionList
