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

# case : the last bet added and clicked playbetslip button, checks mbn and plays calculates total money to be get but don't know if its useful assume already stake given
@app.route('/playbet') 
def playbet(betslip_id = '1' , ): #assume we know the id
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

@app.route('/placeStake') # putting money in the betslip also checks the balance of the player, then gives money 
def placeStake(betslip_id = '1' , stake = 100  ):
    con = connectToDB()
    cur = con.cursor()
    cur.execute("select balance , id from betslip, player  where id = creator_user_id and  betslip_id = %s " , [betslip_id])
    balance = cur.fetchall()
    print(balance[0][0])
    if balance[0][0] >= stake:
        cur.execute("update betslip set stake = %s where betslip_id = %s" , [stake , betslip_id])
        cur.execute("update player set balance = (balance - %s) where id = %s" , [stake , balance[0][1]])
        print("success")
    else:
        print("unsuccessful")
    con.commit()
    form = NameForm()
    return render_template('base.html', form = form)

@app.route('/likeBetslip') # like betslip 
def likebetslip(betslip_id = '1' ):
    con = connectToDB()
    cur = con.cursor()
    cur.execute("update post set no_of_likes = no_of_likes + 1  where betslip_id = %s" , [betslip_id])
    con.commit()
    form = NameForm()
    return render_template('base.html', form = form)

@app.route('/commentonbetslip') # comment on betslip
def commentbetslip(betslip_id = '1' , comment = "selaminaleykum" ):
    con = connectToDB()
    cur = con.cursor()
    cur.execute("select post_id from post where betslip_id = %s" , (betslip_id))
    post_id = cur.fetchall()
    cur.execute("insert into comment values(default ,%s , %s)" , [post_id[0][0] , comment] )
    con.commit()
    form = NameForm()
    return render_template('base.html', form = form)

@app.route('/seefollowers ') # a basic function to get the friends  and to get the posts of the friends
def seefollowersofuser( user_id = '1'  ):
    con = connectToDB()
    cur = con.cursor()
    cur.execute("select followee_id from userfollows where  follower_id = %s" , (user_id))
    followlist = cur.fetchall() # list of people followed by this user 
    cur.execute("select post_id  from post natural join userfollows where post.user_id = userfollows._foll " , [post_id[0][0] , comment] )
    con.commit()
    form = NameForm()
    return render_template('base.html', form = form)

@app.route('/getusernamefromId') # a basic function to user name from the given id 
def getUsernameFromId( user_id = '1'  ):
    con = connectToDB()
    cur = con.cursor()
    cur.execute("select s_name  from suser  where id = %s " , (user_id))
    user_name = cur.fetchall()
    print(user_name)
    con.commit()
    form = NameForm()
    return render_template('base.html', form = form)

@app.route('/getidfromusername') # a basic function to get id from the username 
def getIdFromUsernames( user_name = 'ahmet2'  ):
    con = connectToDB()
    cur = con.cursor()
    cur.execute("select id  from suser  where s_name = %s " , [user_name])
    user_id = cur.fetchall()
    print(user_id)
    con.commit()
    form = NameForm()
    return render_template('base.html', form = form)

@app.route('/getTypeFromUserName') # a basic function to get type of the user from username 
def getTypeFromUsernames( user_name = 'ahmet2'  ):
    con = connectToDB()
    cur = con.cursor()
    cur.execute("select s_type from suser  where s_name = %s " , [user_name])
    user_type = cur.fetchall()
    print(user_type)
    con.commit()
    form = NameForm()
    return render_template('base.html', form = form)

@app.route('/getTypeFromUserID') # a basic function to get type of the user from id of the user
def getTypeFromUserID( user_id = '1'  ):
    con = connectToDB()
    cur = con.cursor()
    cur.execute("select s_type from suser  where id = %s " , [user_id])
    user_type = cur.fetchall()
    print(user_type)
    con.commit()
    form = NameForm()
    return render_template('base.html', form = form)