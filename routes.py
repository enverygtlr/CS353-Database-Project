from flask import render_template, request, flash, Markup, redirect
from forms import RegistrationForm, LoginForm
from lib.config import *
from lib import database as db
import util
import olddb
from app import app

@app.route('/')
def home():
    matches = db.all_matches()
    var = 11
    return render_template('home.html', matches = matches)
# def get_side_bar_user():
#     if not util.session_exists(): # dummy
#         util.session_create(1, 'bombar')
#         util.session_set('selected', [
#             {'team1':'FB', 'team2':'BJK', 'date':'May 3 2020', 'type':'MS1', 'odd':3.1}, 
#             {'team1':'GS', 'team2':'RDE', 'date':'May 6 2020', 'type':'MSX', 'odd':1.5}, 
#             {'team1':'BJK', 'team2':'TS', 'date':'May 4 2020', 'type':'25ALT', 'odd':2.35}])



    # return render_template('side_bar.html', 
    #                         session=util.session_dict(),
    #                         balance=balance,
    #                         stake_form=stake_form)



@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    return render_template('login.html', form = form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    return render_template('register.html', form = form)



""" BOMBAR'S CODE """
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST" and 'username' in request.form:
        username = request.form['username']
        users = olddb.search_by_username(username)
    else:
        users = None
        username = None

    return render_template('search.html', 
                            session=util.session_dict(),
                            users=users,
                            username=username)

@app.route("/remove_selected_bet", methods=["GET"])
def remove_selected_bet():
    if util.session_exists() and 'bet' in request.args:
        index = int(request.args['bet'])
        bets = util.session_get('selected')
        bets.pop(index)
        util.session_set('selected', bets)

    return redirect('/bombar')

@app.route("/play_bet", methods=["GET", "POST"])
def play_bet():
    if util.session_exists() and request.method == "POST" and 'stake' in request.form:
        user_id = util.session_get('user_id')
        stake = int(request.form['stake'])
        balance = olddb.get_user_balance(user_id)

        if stake < balance:
            result = olddb.play_bet(util.session_get('selected'), user_id, stake, False)

            if result is True:
                util.session_set('selected', [])
                return redirect('/bombar')
            else:
                return 'an error occured!'
        else:
            return 'stake cannot be less than balance'
    
    return "wow meen"
