import psycopg2
import psycopg2.extras
import sys
from decimal import *

from datetime import date
import datetime

def connectToPostgres():
    connectionString = 'dbname=%s user=%s password=%s host=%s' % ('bet', 'postgres', 'postgres','localhost')
    try:
        return psycopg2.connect(connectionString)
    except Exception as e:    # BP2 especially this part where you print the exception
        print(type(e))
        print(e)
        print("Can't connect to database")
        return None

def execute(input_query, conn, select=True, args=None):
	cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	
	results = None
	try: 
		sql = cur.mogrify(input_query, args)   # BP6  never use Python concatenation
		                                  # for database queries
		cur.execute(sql)
		if select:
			results = cur.fetchall()
		conn.commit()   # BP5  commit and rollback frequently
	except Exception as e:
		print("failed query", sql)
		conn.rollback()
		print(type(e))
		print(e)
	cur.close()      # BP3 Dispose of old cursors as soon as possible
	return results
""" 
def adminSignup():
    #signing up an admin page 
    con = connectToDB()
    cur = con.cursor()
    cur.execute("select count(*) from admin ")
    templist = cur.fetchall()
    nameExists = False
    try:
        cur.execute("insert into suser values( DEFAULT , %s ,  %s ,%s , %s )  " , ('abdulmuttalip' , 'b' ,'c' , 'admin')) ## a b c yi input olarak alcaz
    except:
        nameExists = True
    if nameExists:
        print("name already taken")
    else:
        print("succesfull sign up of admin")
        cur.execute("insert into admin(id, salary) values((select id from suser where s_name = 'abdulmuttalip'), 102.0);") # buraya da koyuyoruz ismi
    con.commit()
    form = NameForm()
    return render_template('base.html', form = form)


def playerSignup():
    #signing up an a player 
    con = connectToDB()
    cur = con.cursor()
    cur.execute("select count(*) from admin ")
    templist = cur.fetchall()
    nameExists = False
    try:
        cur.execute("insert into suser values( DEFAULT , %s ,  %s ,%s , %s )  " , ('abdulmuzeek' , 'b' ,'c' , 'admin')) ## a b c yi input olarak alcaz
    except:
        nameExists = True
    if nameExists:
        print("name already taken")
    else:
        print("succesfull sign up of player")
        cur.execute("insert into player(id, balance , no_of_followers) values((select id from suser where s_name = 'abdulmuzeek'), 102.0, 0);") # buraya da koyuyoruz ismi
    con.commit()
    form = NameForm()
    return render_template('base.html', form = form)


def editorSignup():
    #signing up an a player 
    con = connectToDB()
    cur = con.cursor()
    cur.execute("select count(*) from admin ")
    templist = cur.fetchall()
    nameExists = False
    try:
        cur.execute("insert into suser values( DEFAULT , %s ,  %s ,%s , %s )  " , ('abdulmuzeek1' , 'b' ,'c' , 'admin')) ## a b c yi input olarak alcaz
    except:
        nameExists = True
    if nameExists:
        print("name already taken")
    else:
        print("succesfull sign up of editor")
        cur.execute("insert into editor(id, salary , success_rate , successful_bets , total_bets , no_of_followers ) values((select id from suser where s_name = 'abdulmuzeek1'), 102.0, 0.5 , 14 , 100 , 12);") # buraya da koyuyoruz ismi
    con.commit()
    form = NameForm()
    return render_template('base.html', form = form)


def adminLogin():
    con = connectToDB()
    cur = con.cursor()
    cur.execute("select * from admin as a natural join suser as b where b.s_name = %s and b.s_password = %s " , ('abdulmuttalip' , 'b')) # username and password
    l = cur.fetchall()
    print(l)
    if len(l) == 1:
        print("success")
    else:
        print("unsuccesful")
    con.commit()
    form = NameForm()
    return render_template('base.html', form = form)

)
def playerLogin():
    con = connectToDB()
    cur = con.cursor()
    cur.execute("select * from player as a natural join suser as b where b.s_name = %s and b.s_password = %s " , ('ahmet2' , 'muzafse2rt')) #usernam and password
    l = cur.fetchall()
    print(l)
    if len(l) == 1:
        print("success")
    else:
        print("unsuccesful")
    con.commit()
    form = NameForm()
    return render_template('base.html', form = form)


def editorLogin():
    con = connectToDB()
    cur = con.cursor()
    cur.execute("select * from editor as a natural join suser as b where b.s_name = %s and b.s_password = %s " , ('abdulmuzeek2' , 'b')) #usernam and password
    l = cur.fetchall()
    print(l)
    if len(l) == 1:
        print("success")
    else:
        print("unsuccesful")
    con.commit()
    form = NameForm()
    return render_template('base.html', form = form)

 """


def get_bet_table(sportbranch="-", league="-", minDate="-"):
  #show all bets given branch, league, mindate
    '''
    returnList = [
        {
            'match_id': 1
            'branch_nane':'football'
            'league_name':'superlig'
            'match_date':'May 3 2020',
            'home_score':0,
            'away_score':0,
            'betslip_date':'May 3 2020',
            't1name':'fenerbahce', 
            't2name':'bursa',
            'bets':[
                {
                    'mnbn':4, 
                    'bet_type':'25ALT', 
                    'cancelled': 0
                    'odd': 4.52
                    'odd_timestamp': 2020-03-12 23:01:25, 
                }
            ]
        }
    ]'''
    
    conn = connectToPostgres()
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
    
    matches = execute(currentBetTableRel, conn, select=True)

  
    resultTable = []

    for match in matches:
        matchId = match["match_id"]

        getBetsQuery = f'''
            select mbn, bet_type, cancelled, odd, odd_timestamp 
            from currentBetView
            where match_id = {matchId} {where_clause}
        '''
        
        bets =  execute(getBetsQuery, conn, select=True)

        match['bets'] = bets

        resultTable.append(match)

    return resultTable

'''
user info
add money

'''

def user_info(userid = '10'):
    if userid is None: return None

    conn = connectToPostgres()
    user_data = execute("select s_type from suser where id = %s " , conn , select=True , args= ([userid]))
    if user_data[0]['s_type'] == 'player':
        player_data = execute("select s_name , email , balance from suser natural join player where id = %s " , conn , select=True , args=([userid])) 
        return player_data[0]['balance']
    elif user_data[0]['s_type'] == 'editor':
        return 'unlimited'
    return None

def findBetId(homeTeam, awayTeam, betType, matchDate):
    conn = connectToPostgres()
    homeTeamIdQuery = f'''
        select team_id from Team where name = \'{homeTeam}\'
    '''
    print(homeTeamIdQuery)
   
    print( execute(homeTeamIdQuery, conn, select=True)[0]['team_id'])
    homeTeamId = execute(homeTeamIdQuery, conn, select=True)[0]['team_id']

    awayTeamIdQuery = f'''
        select team_id from Team where name = \'{awayTeam}\'
    ''' 
    
    awayTeamId =  execute(awayTeamIdQuery, conn, select=True)[0]['team_id']
    print(awayTeamId) 
    matchIdQuery = f'''
        select match_id from match where home_team_id = {homeTeamId} and away_team_id = {awayTeamId} and match_date = \'{matchDate}\'
    '''

    print(matchIdQuery)
    
    matchId = execute(matchIdQuery, conn, select=True)[0]['match_id']

    betIdQuery = f'''
        select bet_id from bet where match_id = {matchId} and bet_type = \'{betType}\'
    '''

    betId = execute(betIdQuery, conn, select=True)[0]['bet_id']

    return betId
#admin queries
def cancel_bet(homeTeam, awayTeam, betType, matchDate):
    conn = connectToPostgres()
  
    betId = findBetId(homeTeam, awayTeam, betType, matchDate)
    
    cancelQuery = f'''
        update bet
        set cancelled = 1
        where bet_id = {betId}
    '''
    print(cancelQuery)

    execute(cancelQuery, conn, select=False)

def update_odds(homeTeam, awayTeam, matchDate, betType, newOdd):
    conn = connectToPostgres()
    betId = findBetId(homeTeam,awayTeam,betType,matchDate)
    print(betId)

    timestamp = datetime.datetime.now().replace(microsecond=0)

    insertQuery = f'''
        insert into odd(odd, odd_timestamp, bet_id)
        values({newOdd}, \'{timestamp}\',{betId});
    '''
    print(insertQuery)
    
    execute(insertQuery, conn, select=False)

def getBetsOfBetslip(betslip_id):
    conn = connectToPostgres()
    betSelectQuery = f'''
        with oddofbet as 
        (select   bet_id, t1.name as t1name, t2.name as t2name , bet_type , mbn,  max(odd_timestamp) as odd_timestamp, match_date
        from betslip natural join betsliphas natural join bet natural join odd natural join match , team as t1 , team as t2 
        where betslip_id = {betslip_id} and home_team_id = t1.team_id  and away_team_id = t2.team_id and odd_timestamp < betslip_date
        group by  bet_id, t1name, t2name , mbn, bet_type, match_date)
        select * 
        from oddofbet natural join odd
    '''

    betList = execute(betSelectQuery, conn, select=True)

    return betList

def get_user_betslips(user_id, include_private=False):
    '''
    betslipList = [
        {
            'betslip_id': 3,
            'stake', Decimal('150.50')),
            'total_odd', None), 
            'betslip_date', datetime.datetime(2022, 2, 21, 11, 32, 23))
            'bet':
                [
                   {
                       ('bet_id', 11), 
                       ('odd_timestamp', datetime.datetime(2020, 3, 11, 22, 11, 25)), 
                       ('t1name', 'galatasaray'), 
                       ('t2name', 'fenerbahce'),
                       ('bet_type', 'MS 2'),
                       ('mbn', 3), 
                       ('match_date', datetime.datetime(2020, 2, 19, 0, 0)), 
                       ('odd', Decimal('3.50')), 
                       ('cancelled', 0)

                   }
                ]
        }
    ]
    '''
    conn = connectToPostgres()
    sharedBet = ''
    if include_private == False:
        sharedBet = 'and shared = 1'

    betslipQuery = f'''
        select betslip_id, stake, total_odd, betslip_date
        from betslip
        where creator_user_id = {user_id} {sharedBet}
    '''
    
    
    betslipList = execute(betslipQuery, conn, select=True)
    
    betslipIdQuery = f'''
        select betslip_id
        from betslip
        where creator_user_id = {user_id}
    '''

    betslipIdList= execute(betslipIdQuery, conn, select=True)
    resultTable = []


    for betslip in betslipList:
        betslip['bet'] = getBetsOfBetslip(betslip['betslip_id'])
        resultTable.append(betslip)

    print(resultTable)
    return resultTable

def delete_user(user_id):
    conn = connectToPostgres()
    query = f'''delete from suser where id = {user_id};'''
    execute(query, conn, select=False)

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
    conn = connectToPostgres()

    query = f'''
        with followed_user_ids as 
        (select followee_id as followed_id, s_name
        from userfollows, suser
        where follower_id = {user_id}  and id = followee_id)
        select * from followed_user_ids,post where user_id = followed_id
    '''
    
    postTable = execute(query, conn, select=True)

    resultTable = []
    
    for post in postTable:
        betslipQuery = f'''
            select betslip_id, stake, total_odd, betslip_date
            from betslip where betslip_id = {post['betslip_id']};
        '''

        print(post)
          
        betslip = execute(betslipQuery, conn, select=True)[0]
        betslip['bets'] = getBetsOfBetslip(post['betslip_id'])

        post['betslip'] = betslip

        commentQuery = f'''
            select s_name, context
            from (comment natural join post) , suser 
            where post_id = {post['post_id']} and id = commenter_id;
        '''

        post['comment'] = execute(commentQuery, conn, select=True)

        resultTable.append(post)

    return resultTable

def get_suggestions_by_user(user_id):
    '''
    suggestionList = 
    [
        {
            ('s_name', 'editor1'),
            ('bet_id', 7),
            ('user_id', 10),
            ('trust', 10),
            ('shared_content', 'banko bet'),
            ('match_id', 3), ('mbn', 5),
            ('bet_type', 'ALT'), 
            ('odd_timestamp', datetime.datetime(2020, 3, 12, 23, 1, 25)), 
            ('odd', Decimal('0.01')),
            ('cancelled', 0), 
            ('team1', 'trabzon'), 
            ('team2', 'besiktas')
        }
    ]
    '''
    conn = connectToPostgres()

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

    suggestionList = execute(query, conn, select=True)

    for suggestion in suggestionList:
        matchId = suggestion['match_id']

        teamQuery = f'''
            select t1.name as t1name, t2.name as t2name
            from match, team as t1, team as t2
            where match_id = {matchId} and home_team_id = t1.team_id and away_team_id = t2.team_id
        '''

        teams = execute(teamQuery, conn, select=True)[0]

        suggestion['team1'] = teams['t1name']
        suggestion['team2'] = teams['t2name']

    
    print(suggestionList)
    return suggestionList


def get_suggestions_by_editor(editor_id):
    '''
    suggestionList = 
    [
        {
            ('s_name', 'editor1'),
            ('bet_id', 7),
            ('user_id', 10),
            ('trust', 10),
            ('shared_content', 'banko bet'),
            ('match_id', 3), ('mbn', 5),
            ('bet_type', 'ALT'), 
            ('odd_timestamp', datetime.datetime(2020, 3, 12, 23, 1, 25)), 
            ('odd', Decimal('0.01')),
            ('cancelled', 0), 
            ('team1', 'trabzon'), 
            ('team2', 'besiktas')
        }
    ]
    '''

    conn = connectToPostgres()
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


def delete_post(user_id, betslip_id):
    #update shared status
    conn = connectToPostgres()
    sharedQuery = f'''
        update betslip set shared = 0 where betslip_id = {betslip_id};
    '''
    execute(sharedQuery, conn, select=False)

    deletePostQuery = f'''
        delete from post where betslip_id = {betslip_id} and user_id = {user_id};
    '''  

    execute(deletePostQuery, conn, select=False) 


def create_post(user_id, betslip_id):
    #update shared status
    conn = connectToPostgres()
    sharedQuery = f'''
        update betslip set shared = 1 where betslip_id = {betslip_id};
    '''
    execute(sharedQuery, conn, select=False)

    currentdate = datetime.datetime.now().replace(microsecond=0)

    #create post query
    createPostQuery = f''' 
        insert into Post(no_of_people_played, betslip_id, user_id, no_of_likes, post_date)
        values(0, {betslip_id}, {user_id}, 0, \'{currentdate}\')
    '''
    execute(createPostQuery, conn, select=False) 
    
    


def get_user_balance(user_id = '1'):
    conn  = connectToPostgres()
    queryString = "select balance from player where id  = %s "
    balance = execute(queryString, conn , select=True , args = ([user_id]))
    print(balance[0]["balance"])
    return balance

def get_all_followers(user_id = '2'):
    conn = connectToPostgres()
    queryString = "select follower_id , s_name from userfollows , suser where followee_id = %s and follower_id = id "
    follower_table = execute(queryString ,conn , select= True , args = ([user_id]))
    print(follower_table)
    return follower_table 

def get_all_followee(user_id = '1'):
    conn = connectToPostgres()
    queryString = "select followee_id , s_name from userfollows , suser where follower_id = %s and followee_id = id "
    followee_table = execute(queryString , conn , select = True , args = ([user_id]))
    return followee_table 

def update_shared_status(betslip_id = '3'):
    conn = connectToPostgres()
    queryString = "update betslip set shared = 1  where  betslip_id = %s "
    execute(queryString , conn , select=False , args = [betslip_id])
    queryString = "select creator_user_id from betslip  where betslip_id = %s "
    user_id = execute(queryString , conn , select= True , args = ([betslip_id]))
    currentdate = datetime.datetime.now()
    print(betslip_id)
    print(user_id[0]["creator_user_id"])
    print(currentdate)
    queryString = "insert into post values(default , 0, %s , %s , 0 , %s  )"
    execute(queryString , conn , select=False , args=([betslip_id , user_id[0]["creator_user_id"], currentdate]) )

def editor_suggests(editor_id = '1' , bet_id = "4" , comment = "cok iyi bet" , trust = '20'):
    conn = connectToPostgres()
    #get the match id
    queryString =  "select match_id , bet_id from bet natural join editor_suggests where user_id = %s   "
    matchandbets = execute(queryString , conn , select=True , args = ([editor_id]))
    queryString = "select match_id  from bet  where bet_id = %s "
    match_id = execute(queryString , conn , select=True , args = ([bet_id]))
    queryString = "select * from editor_suggests natural join match where  user_id = %s and match_id = %s "
    similiarsuggests = execute(queryString , conn , select=True , args= ([ editor_id,match_id[0]["match_id"]]))
    if len(similiarsuggests) == 0:
        execute("insert into editor_suggests values(%s , %s , %s , %s ) ",conn , select = False, args=([bet_id , editor_id , trust, comment] ))
    else:
        print("you already suggested one bet from the match ")

def search_by_username(username = "ahmet3"):
    conn = connectToPostgres()
    queryString = "select s_name, id , no_of_followers  from player natural join suser where s_name ~ %s "
    players_data = execute(queryString , conn , select=True , args= ([username]))
    queryString = "select s_name, id , no_of_followers  from editor natural join suser where s_name ~ %s "
    editors_data = execute(queryString , conn , select=True , args= ([username]))
    return players_data + editors_data

def follow_user(user_id = '2', requested_user_id = '10'):
    conn = connectToPostgres()
    queryString = "select * from userfollows where  follower_id = %s and followee_id = %s "
    data = execute(queryString,conn , select=True , args = ([user_id , requested_user_id]))
    print(data)
    if len(data) == 0:
        execute("insert into userfollows values( %s , %s )" , conn , select=False ,args=([user_id, requested_user_id]) )
        queryString = "select s_type from suser where id = %s "
        user_type = execute(queryString , conn , select=True , args=([requested_user_id]))
        if user_type[0]["s_type"] == "editor":
            execute("update editor set no_of_followers = no_of_followers + 1 where id = %s " , conn ,select=False  , args=([requested_user_id]))
        elif user_type[0]["s_type"] == "player":
            execute("update player set no_of_followers = no_of_followers + 1 where id = %s ", conn , select=False , args=([requested_user_id]))
        return True
    else:
        return False
        print("muzo")

def add_comment_to_post(user_id= '1', post_id = '3', comments = ''):
    conn = connectToPostgres()
    execute("insert into comment values(default , %s,  %s  , %s)" , conn , select=False, args=([post_id, user_id, comments]))

def like_post(user_id ='1', post_id = '3'):
    conn = connectToPostgres()
    likes = execute("select * from postlikes where user_id = %s and post_id = %s " , conn , select=True ,  args=([user_id , post_id]))
    if len(likes) == 0 : #like the post 
        execute("insert into postlikes values(%s , %s)" , conn ,select=False, args=([post_id,user_id]) )
        execute("update post set no_of_likes = no_of_likes + 1  where post_id = %s ", conn ,select=False, args = [post_id])
        return True 
    else: #post already has been liked 
        return False 

def selectBet( bet_id = '3' , betslip_id = '1' ):
     conn = connectToPostgres()
     table = execute("select *  from betSlipHas where betslip_id = %s and bet_id = %s"  ,conn , select= True, args =([betslip_id , bet_id]))
     canceled = execute("select cancelled from bet where bet_id = %s" , conn  , select=True , args = ([bet_id]))
     if len(table) == 0 and canceled[0]["cancelled"] == 0: # meaning the bet is not inside the betslip.
         execute("insert into BetSlipHas values(%s , %s )" , conn , select=False , args =([betslip_id , bet_id]))
         print("added")
     else: 
         print("can't added")
         return False
  

def playBet(betslip_id = '1', user_id= '1'): #assume we know the id
    conn = connectToPostgres()
    maximumMbn = execute("select max(mbn), count(*) from betsliphas natural join bet where betslip_id = %s", conn , select = True,args =([betslip_id]))
    print(maximumMbn)
    totalMoneyWon = 0
    if maximumMbn[0]["max"] > maximumMbn[0]["count"] :
        deleteBelslipQuery = f'''
            delete from betslip where betslip_id = {betslip_id};
        '''
        execute(deleteBelslipQuery, conn, select=False)

        return False,"mbn is too high can't do that."

    else: 
        print("you play the bet")
        totalMoneyWon = execute("select total_odd , stake from betslip where betslip_id = %s ",conn , select = True  , args=([betslip_id]))
        money = totalMoneyWon[0]["total_odd"]  * totalMoneyWon[0]["stake"]

        #update balance of according to success of betslip
        if isbetslipSuccesful(betslip_id):
            print('Bet successful')
            old_balance = get_user_balance(user_id)[0]['balance']
            new_balance = money + old_balance
            updateQuery = f'''
                update player set balance = {new_balance} where id = {user_id};
             '''
            execute(updateQuery, conn, select=False)
        else:
            #money is lost
            print('Bet is not successful')
            old_balance = get_user_balance(user_id)[0]['balance']
            new_balance = old_balance - totalMoneyWon[0]["stake"]
            updateQuery = f'''
                update player set balance = {new_balance} where id = {user_id};
            '''
            execute(updateQuery, conn, select=False) 

   
   
    return True,'Betslip is created.'
         # played here
         # I don't kow what to do with the total money 
         #perhaps useful in another query 

def play_bet(list_bets = [{'team1':'fenerbahce', 'team2':'bursa', 'date':'2019-02-19 00:00:00', 'type':'1.5 ALT'}], user_id = '5', stake = '10', shared='0'):
    #get the bets from list_bets
    conn = connectToPostgres()
    #get user type
    userTypeQuery = f''' 
        select s_type
        from suser
        where id = {user_id};
    '''
    userType = execute(userTypeQuery, conn, select=True)[0]['s_type']

    if userType == 'player':
        #check balance
        balance = get_user_balance(user_id)[0]['balance']

        if stake > balance:
            return False,'Balance is not enough.'


    currentdate = datetime.datetime.now().replace(microsecond=0)
    #create our betslip
    execute("insert into betslip values(default , %s ,%s , %s , %s, 1.0  ) ", conn, select=False, args=([user_id, stake, shared, currentdate]))
    
    betslipIdQuery = f'''
        select betslip_id 
        from betslip
        where betslip_date = \'{currentdate}\' and creator_user_id = {user_id};
     '''

    betslip_id = execute(betslipIdQuery, conn , select=True)
    betslip_length = len(list_bets)
    for i in range(betslip_length):
        team1 = list_bets[i]["t1name"]
        team2 = list_bets[i]["t2name"]
        date = list_bets[i]["match_date"]
        match_type = list_bets[i]["bet_type"]
        team1_id = execute("select team_id from team where name = %s " ,conn , select = True, args = [(team1)])
        team2_id = execute("select team_id from team where name = %s " , conn , select = True , args = ([team2]))
        bet_id = execute("select bet_id from bet natural join match where home_team_id = %s and away_team_id = %s and match.match_date = %s and bet_type = %s" , conn ,select = True ,  args=([team1_id[0]["team_id"] , team2_id[0]["team_id"] , date , match_type ]))
        selectBet(bet_id[0]["bet_id"], betslip_id[0]["betslip_id"])
    
    total_odd = (Decimal(calculateTotalOdd(betslip_id[0]["betslip_id"])).quantize(Decimal('.01'), rounding=ROUND_DOWN))
    execute("update betslip set total_odd = total_odd * %s where betslip_id  = %s " , conn , select = False ,args = (total_odd , betslip_id[0]['betslip_id']))

    if userType == 'editor':
        create_post(user_id, betslip_id[0]['betslip_id'])
        return True, 'Editor added betslip'
    
    return playBet(betslip_id[0]["betslip_id"], user_id)

# TODO: ALAHhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
def user_register(username, email, password, user_type='player' ):
    #signing up an admin page 
    conn = connectToPostgres()
    redundant_data = execute("select id from suser where s_name = %s or email = %s " , conn , select = True , args=([username , email ]))
    if len(redundant_data) == 0: # no data exists for username and password 
        execute("insert into suser values(default , %s , %s ,%s , %s )" , conn , select=False , args=([username, password, email, user_type]) )
        user_id = execute("select id from suser where s_name = %s " , conn , select = True , args =([username]))
        if user_type == 'player':
            execute("insert into player values(%s , 0 , 0 )" , conn , select=False , args=([user_id[0]["id"]]) )
        elif user_type == 'editor':
            execute("insert into editor values(%s , 4000 , 0 , 0 ,0 , 0 )" , conn , select=False , args=([user_id[0]["id"]]) )
        elif user_type == 'admin':
            execute("insert into admin values(%s , 4000  )" , conn , select=False , args=([user_id[0]["id"]]) )
        return True, ''
    else:
        return False, "username or mail has already been taken"

def login_check(username,  password):
    conn = connectToPostgres()
    data = execute("select * from suser where s_name = %s and s_password = %s  " , conn , select = True , args = ([username , password]) )
    if len(data) == 0:
        return False , None
    else:
        return True, {'username':data[0]['s_name'], 
                        'user_id':data[0]['id'], 
                        'password':data[0]['s_password'], 
                        'email':data[0]['email'], 
                        'type':data[0]['s_type'] }


def calculateTotalOdd(betslip_id):
    betslipList = getBetsOfBetslip(betslip_id)

    total_odd = 1

    for betslip in betslipList:
        print(betslip['odd'])
        total_odd *= betslip['odd']

    return total_odd

def isBetSuccessful(bet_id = '1' , sport_branch  = 'football'):
    conn = connectToPostgres()
    betData = execute("select bet_type , home_score , away_score from bet natural join match where bet_id = %s " , conn , select=True,  args = ([bet_id]) )
    print(betData)
    # now need to know what bet_type is depend on there insert your boolean values and get the result
    if sport_branch == 'football':
        if betData[0]["bet_type"] == "1.5 UST":
            if betData[0]["home_score"] + betData[0]["away_score"] > 1:
                print("successful")
                return True
            else:
                print("unsuccessful")
                return False
        elif betData[0]["bet_type"] == "1.5 ALT":  
            if betData[0]["home_score"] + betData[0]["away_score"] <= 1:
                print("successful")
                return True
            else:
                print("unsuccessful")
                return False
        elif betData[0]["bet_type"] == "2.5 UST":
            if betData[0]["home_score"] + betData[0]["away_score"] > 2:
                print("successful")
                return True
            else:
                print("unsuccessful")
                return False
        elif betData[0]["bet_type"] == "2.5 ALT":  
            if betData[0]["home_score"] + betData[0]["away_score"] <= 2:
                print("successful")
                return True
            else:
                print("unsuccessful")
                return False
                
    elif sport_branch == 'basketball':
        print("not yet decided")
    elif sport_branch == 'tennis':
        print("not yet decided")
    
    if betData[0]["bet_type"] == "MS 1":
        if betData[0]["home_score"] > betData[0]["away_score"]:
            return True
            print("succesfull")
        elif betData[0]["home_score"] < betData[0]["away_score"]:
            return False
            print('unsuccesful')
   
    if betData[0]["bet_type"] == "MS 2":
        if betData[0]["home_score"] > betData[0]["away_score"]:
            return False
            print("unsuccesfull")
        elif betData[0]["home_score"] < betData[0]["away_score"]:
            return True
            print('succesful')
    
    if betData[0]["bet_type"] == "MS X":
        if betData[0]["home_score"] == betData[0]["away_score"]:
            return True
            print("succesfull")
        else:
            return False
            print('unsuccesful')

def isbetslipSuccesful(betslip_id = '1'):
    conn = connectToPostgres()
    betslip = execute("select bet_id from betslip natural join betsliphas where betslip_id = %s " , conn, select=True , args = ([betslip_id]))

    for i in range(len(betslip)):
        bet_id = betslip[i]["bet_id"]
        branch_name = execute("select branch_name from bet natural join (match natural join league) where bet_id = %s ", conn , select=True , args = ([bet_id]))

        print(bet_id, branch_name)

        if isBetSuccessful(bet_id,branch_name[0]["branch_name"]) != True: #valla size birakiyorum karari bu fonksiyon boolean mi dondursun falan filan, duruma
            return False

    return True


def get_like_back(user_id = '6' ,  post_id = '3'):
    conn = connectToPostgres()
    execute("delete  from postlikes where  user_id = %s and post_id = %s " , conn , select= False , args = ([user_id , post_id]))
    execute("update post  set no_of_likes = no_of_likes - %s where post_id = %s " , conn , select=False , args =([ 1 , post_id]) )