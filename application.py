from flask import * 
from flask_bootstrap import Bootstrap
import database as db
from util import redirect_last, convert_smatch
from forms import *


app = Flask(__name__)
boot = Bootstrap(app)

app.secret_key = '9c543e044e10b6e0bfb7'

# start of pages

@app.route('/', methods=["GET", "POST"])
def home_page():
    loggedin = session.get('loggedin') # True if exists else None
    matches = db.get_bet_table()
    selected = session.get('selected')
    balance = 100 # db.get_user_balance(session['user_id']) if session.get('user_id') is not None else None
    
    form = PlayBetForm()

    if form.validate_on_submit() and loggedin is not None:
        stake = form.stake.data
        count = len(selected)

        # validate selected bets ????

        validated = stake > 0 and stake < balance

        if validated:
            flash('Bet is played successfully!')
            session['selected'] = []

            # update balance
            # update user bets
            return redirect('/')
        else:
            flash('Please play with a lower stake', 'error')
            return redirect_last()        

    return render_template('homepage.html', 
                            loggedin=loggedin,
                            matches=matches,
                            selected=selected,
                            balance=balance,
                            form=form)

@app.route('/login', methods=["GET", "POST"])
def login_page():
    loggedin = session.get('loggedin')

    if loggedin is not None: return redirect('/')

    form = LoginForm()

    if form.validate_on_submit():
        validated = db.login_check(form.email.data, form.password.data)

        if validated:
            username, user_id = db.get_name_id(form.email.data)
            
            session['username'] = username
            session['user_id']  = user_id
            session['loggedin'] = True
            session['selected'] = []

            return redirect('/') # redirect to home
        else:
            flash('Worng username or password', 'error')

    return render_template('loginpage.html', 
                            loggedin=None,
                            form=form)

@app.route('/register', methods=["GET", "POST"])
def register_page():
    loggedin = session.get('loggedin')

    if loggedin: flash('Please log out before registering')
    
    form = RegistrationForm()

    if form.validate_on_submit():
        validated = not db.register_check(form.email.data)

        if validated:
            flash('Account created, please login')
            db.create_user(form.fullname.data, form.password.data, form.email.data)
        else:
            flash('Cannot create account, email already registered', 'error')
        

    return render_template('registerpage.html', 
                            loggedin=loggedin,
                            form=form)

@app.route('/profile')
def profile_page():
    return ''

@app.route('/feed')
def feed_page():
    return ''

@app.route('/suggestions')
def suggestions_page():
    return ''

@app.route('/search')
def search_page():
    return ''

# end of pages 
# start of functions

@app.route('/logout')
def logout_page():
    session.clear()
    return redirect_last()

@app.route('/remove_selected_bet', methods=["GET", "POST"])
def remove_selected_bet(): # bet
    if session.get('loggedin') is None: return redirect_last()

    try:
        bet = int(request.args.get('bet'))
    except:
        return redirect_last()

    selected = session.get('selected') # should return a list

    selected.pop(bet)

    session['selected'] = selected

    return redirect_last()

@app.route('/add_selected_bet', methods=["GET", "POST"])
def add_selected_bet(): # row, col
    if session.get('loggedin') is None: return redirect_last()

    try:
        row = int(request.args.get('row'))
        col = int(request.args.get('col'))
    except:
        return redirect_last()
    
    matches = db.get_bet_table()
    selected_match = None
    selected = list(session['selected'])

    for i, match in enumerate(matches):
        for j, bet in enumerate(match['bets']):
            if col != j or row != i:  continue
            selected_match = convert_smatch(match)[j] # badfix

    if selected_match is None: redirect('/') # this should not happen



    selected.append(selected_match)
    session['selected'] = selected

    return redirect_last()  

# end of functions