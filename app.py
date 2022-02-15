from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_session import Session
import psycopg2
import psycopg2.extras
import sys



    

print('your mom')

def connectToDB():
    print('buraya geldim mi')
    connectionString = 'dbname=bet user=postgres password=postgres host=localhost'
    print(connectionString)
    try:
        return psycopg2.connect(connectionString)
        print('connected to db')
       
    except:
        print("cant connect to db")        


conn = connectToDB()
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

app.config["SESSION PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
notes =[]

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = connectToDB()
    cur = conn.cursor()
    try:
        cur.execute("select * from suser")
    except:
        print("error running sql")
    results = cur.fetchall()
    print(results)
    name = None
    form = NameForm()
    if session.get("notes") is None:
        session["notes"] = []

    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    
    creators = ["Batuhan", "Berk", "Bombar", "Enver"]
    if request.method == "POT":
        note = request.form.get("note")
        session["notes"].append(note)
    return render_template('index.html', form=form, name=name, creators = results, notes = session["notes"])

@app.route('/user/query')
def user():
    getAllBetSlipsOfUser(1)

    getBetsOfBetslip(2)

    #     cancelBet('trabzon','besiktas','ALT','2019-02-19 00:00:00')
    #   # changeOddOfBet('goztepe','altay','MS X', '2020-02-19 00:00:00', 1.13, '2019-03-19 11:23:00')        

    #     print('query')
    #     conn = connectToDB()
    #     cur = conn.cursor()


    return render_template('500.html')
        
        


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
        select t1name, t2name, mbn, bet_type, odd, cancelled, match_date
        from currentBetView
        where 1=1 {where_clause}
    '''

    try:
        cur.execute(currentBetTableRel)
    except:
        print("error running sql")
    
    results = cur.fetchall()

    for row in results:
        print(row)

    return results

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

def getBetsOfBetslip(betslip_id):
    betSelectQuery = f'''
        with oddofbet as 
        (select   bet_id, t1.name as t1name, t2.name as t2name , mbn, bet_type , max(odd_timestamp) as odd_timestamp
        from betslip natural join betsliphas natural join bet natural join odd natural join match , team as t1 , team as t2 
        where betslip_id = 2 and home_team_id = t1.team_id  and away_team_id = t2.team_id and odd_timestamp < betslip_date
        group by  bet_id, t1name, t2name , mbn, bet_type)
        select * 
        from oddofbet natural join odd
    '''
    try:
        cur.execute(betSelectQuery)
    except:
        print("error running sql")
        
    betList = cur.fetchall()

    for row in betList:
        print(row)

    return betList


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


def changeOddOfBet(homeTeam, awayTeam, betType, matchDate,newOdd, timestamp):
    betId = findBetId(homeTeam,awayTeam,betType,matchDate)
    print(betId)

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

