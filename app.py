from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_session import Session
import psycopg2
import psycopg2.extras
import datetime
print('your mom')
def connectToDB():
    print('buraya geldim mi')
    connectionString = 'dbname=bet user=dev password=dev host=localhost'
    print(connectionString)
    try:
        print('connected to db')
        return psycopg2.connect(connectionString)
    except:
        print("cant connect to db")
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
    if request.method == "POST":
        note = request.form.get("note")
        session["notes"].append(note)
    return render_template('index.html', form=form, name=name, creators = results, notes = session["notes"])

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name= name)
@app.route('/signingupadmin')
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
@app.route('/signingupplayer')
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
@app.route('/signingupeditor')
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
@app.route('/loginadmin')
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
@app.route('/loginplayer')
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
@app.route('/logineditor')
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
@app.route('/getallmatches') # all matches without filters
def getAllMatches():
    con = connectToDB()
    cur = con.cursor()
    cur.execute("select * from match " ) #usernam and password
    matchlist = cur.fetchall()
    for i in range( len(matchlist)):
        #get the name of the teams
        cur.execute("select name from team where team_id = %s " , [matchlist[i][1]])
        name1 = cur.fetchall()
        cur.execute("select name from team where team_id = %s " , [matchlist[i][2]] )
        name2 = cur.fetchall()
        print("match is between " ,name1[0][0], "and " , name2[0][0] )
    print( matchlist)
    con.commit()
    form = NameForm()
    return render_template('base.html', form = form)


# query the bet coming from odd  ( 1.c )
@app.route('/selectbet')
def selectBet( bet_id = '3' , betslip_id = '1' ):
     con = connectToDB()
     cur = con.cursor()
     cur.execute("select odd from odd natural join bet where bet_id =  %s " , [bet_id]) # we got the bet_id 
     odd = cur.fetchall()
     cur.execute("select *  from betSlipHas where betslip_id = %s and bet_id = %s"  , [betslip_id , bet_id])
     table = cur.fetchall()
     cur.execute("select cancelled from bet where bet_id = %s" , [bet_id])
     canceled = cur.fetchall()
     form = NameForm()
     if len(table) == 0 and canceled[0][0] == 0: # meaning the bet is not inside the betslip.
         cur.execute("insert into BetSlipHas values(%s , %s )" , [betslip_id , bet_id])
         print("added")
     else: 
         print("can't added")
         return render_template('base.html', form = form)
     cur.execute("update betslip set total_odd = total_odd * %s where betslip_id  = %s " , [odd[0][0] , betslip_id])
     con.commit()
     return render_template('base.html', form = form)

# case : the last bet added and clicked playbetslip button, checks mbn and plays calculates total money to be get but don't know if its useful
@app.route('/playbet') 
def playbet(betslip_id = '1'): #assume we know the id
    con = connectToDB()
    cur = con.cursor()
    cur.execute("select max(mbn), count(*) from betsliphas natural join bet where betslip_id = %s" ,[betslip_id])
    maximumMbn = cur.fetchall()
    print(maximumMbn)
    totalMoneyWon = 0
    if maximumMbn[0][0] > maximumMbn[0][1] :
        print("mbn is too high can't do that ")
    else: 
        print("you play the bet")
        cur.execute("select total_odd , stake from betslip where betslip_id = %s " , [betslip_id])
        totalMoneyWon = cur.fetchall()
        money = totalMoneyWon[0][0] * totalMoneyWon[0][1]
        print("money won is ", money)
         # played here
         # I don't kow what to do with the total money 
         #perhaps useful in another query 
    con.commit()
    form = NameForm()
    return render_template('base.html', form = form)

# to see if betslip has ended and if it's ended to see if it is won or lost
@app.route('/isplayedbetslip')
def isPlayedBetslip(betslip_id = '1' ): # with betslip id 
    #get the maximum date of the betslip
    con = connectToDB()
    cur = con.cursor()
    cur.execute("select max(match_date) from match")
    maxdate = cur.fetchall()
    print(maxdate[0][0])
    #check if time has passeds
    currentdate = datetime.datetime.now()
    if currentdate > maxdate[0][0]: #betslip is known if it's won or lost 
        print("it is over")
        # oynanmis 
    else:
        print("its not over yet")
        #oynanmamis, buralara frontendde boolean yerlestirilip ona gore ne kazandigina bkailabilir 
    con.commit()
    form = NameForm()
    return render_template('base.html', form = form)
@app.route('/isplayedmatch')
def isPlayedMatch(match_id = '1' ): # with betslip id 
    #get the maximum date of the betslip
    con = connectToDB()
    cur = con.cursor()
    cur.execute("select match_date from match where match_id = %s" , [match_id])
    maxdate = cur.fetchall()
    print(maxdate[0][0])
    #check if time has passeds
    currentdate = datetime.datetime.now()
    con.commit()
    form = NameForm()
    if len(maxdate) == 0:
        print("match id not found")
       
        return render_template('base.html', form = form)
    if currentdate > maxdate[0][0]: #betslip is known if it's won or lost 
        print("it is over")
        # oynanmis 
    else:
        print("its not over yet")
        #oynanmamis, buralara frontendde boolean yerlestirilip ona gore ne kazandigina bkailabilir 
    return render_template('base.html', form = form)

@app.route('/isBetSuccessful') #shallbe invoked after only knowing that match is played, isplayedmatch()
def isBetSuccessful(bet_id = '1' , sport_branch  = 'football'):
    con = connectToDB()
    cur = con.cursor()
    cur.execute("select bet_type , home_score , away_score from bet natural join match where bet_id = %s " , [bet_id])
    betData = cur.fetchall()
    print(betData)
    # now need to know what bet_type is depend on there insert your boolean values and get the result
    if sport_branch == 'football':
        if betData[0][0] == "1.5 UST":
            if betData[0][1] + betData[0][2] > 1:
                print("successful")
            else:
                print("unsuccessful")
        elif betData[0][0] == "1.5 ALT":  
            if betData[0][1] + betData[0][2] <= 1:
                print("successful")
            else:
                print("unsuccessful")
        elif betData[0][0] == "2.5 UST":
            if betData[0][1] + betData[0][2] > 2:
                print("successful")
            else:
                print("unsuccessful")
        elif betData[0][0] == "2.5 ALT":  
            if betData[0][1] + betData[0][2] <= 2:
                print("successful")
            else:
                print("unsuccessful")
    elif sport_branch == 'basketball':
        print("not yet decided")
    elif sport_branch == 'tennis':
        print("not yet decided")
    if betData[0][0] == "MS1":
        if betData[0][1] > betData[0][2]:
            print("succesfull")
        elif betData[0][1] < betData[0][2]:
            print('unsuccesful')
    if betData[0][1] == "MS2":
        if betData[0][1] > betData[0][2]:
            print("unsuccesfull")
        elif betData[0][1] < betData[0][2]:
            print('succesful')
    if betData[0][0] == "MSX":
        if betData[0][1] == betData[0][2]:
            print("succesfull")
        else:
            print('unsuccesful')
    con.commit()
    form = NameForm()
    return render_template('base.html', form = form)

@app.route('/isBetslipSuccesful') # shall check after isplayedbetslip may cause error otherwise 
def isbetslipSuccesful(betslip_id = '1'):
    con = connectToDB()
    cur = con.cursor()
    cur.execute("select bet_id from betslip natural join betsliphas where betslip_id = %s " , [betslip_id])
    betslip = cur.fetchall()
    print(betslip)
    print(len(betslip))
    for i in range(len(betslip)):
       bet_id = betslip[i][0]
       cur.execute("select branch_name from bet natural join (match natural join league) where bet_id = %s " , [bet_id])
       branch_name = cur.fetchall()
       isBetSuccessful(bet_id,branch_name[0][0]) #valla size birakiyorum karari bu fonksiyon boolean mi dondursun falan filan, duruma
       print(bet_id)
       print(branch_name[0][0])

    con.commit()
    form = NameForm()
    return render_template('base.html', form = form)
