from flask import * 
from flask_bootstrap import Bootstrap
import databasev2 as db
from util import *
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
    user_id = session.get('user_id')
    username = session.get('username')
    balance = None 

    if loggedin is not None:
        balance = db.user_info(session['user_id'])

    form = PlayBetForm()

    if form.validate_on_submit() and loggedin is not None:
        stake = form.stake.data
        count = len(selected)

        success, message = db.play_bet(selected, user_id, stake, 0)

        if success:
            session['selected'] = []
            flash(message)
            return redirect('/')
        else:
            flash(message, 'error')
            return redirect('/')  

    return render_template('homepage.html', 
                            loggedin=loggedin,
                            matches=matches,
                            selected=selected,
                            balance=balance,
                            form=form,
                            username=username)

@app.route('/login', methods=["GET", "POST"])
def login_page():
    loggedin = session.get('loggedin')
    username = session.get('username')

    if loggedin is not None: return redirect('/')

    form = LoginForm()

    if form.validate_on_submit():
        validated, dictionary = db.login_check(form.username.data, form.password.data)

        if validated:            
            session['username'] = dictionary['username']
            session['user_id']  = dictionary['user_id']
            session['user_type']  = dictionary['type']
            session['type'] = dictionary['type']
            session['loggedin'] = True
            session['selected'] = []

            return redirect('/') # redirect to home
        else:
            flash('Wrong username or password', 'error')

    return render_template('loginpage.html', 
                            loggedin=None,
                            form=form,
                            username=username)

@app.route('/register', methods=["GET", "POST"])
def register_page():
    loggedin = session.get('loggedin')
    username = session.get('username')

    if loggedin: flash('Please log out before registering')
    
    form = RegistrationForm()

    if form.validate_on_submit():
        validated, message = db.user_register(form.fullname.data, form.email.data, form.password.data, form.typee.data)

        if validated:
            flash('Account created, please login', 'message')
        else:
            flash(message, 'error')
        

    return render_template('registerpage.html', 
                            loggedin=loggedin,
                            form=form,
                            username=username)

@app.route('/profile')
def profile_page():
    return ''

@app.route('/feed')
def feed_page():
    loggedin = session.get('loggedin')
    username = session.get('username')
    posts = None

    if loggedin is not None:
        user_id = session.get('user_id')
        posts = db.get_feed_posts(user_id)
        
    return render_template('feedpage.html', 
                            loggedin=loggedin,
                            posts=posts,
                            username=username)

@app.route('/suggestions')
def suggestions_page():
    return ''

@app.route('/search', methods=["GET", "POST"])
def search_page():
    loggedin = session.get('loggedin')
    username = session.get('username')
    form = SearchForm()
    users = None
    search_key = None

    if form.validate_on_submit(): # when actually searched
        users = db.search_by_username(form.search.data)
        search_key = form.search.data

    return render_template('searchpage.html', 
                            loggedin=loggedin,
                            form=form,
                            users=users,
                            search_key=search_key,
                            username=username)

@app.route('/users/<pname>', methods=["GET", "POST"])
def user_page(pname):
    loggedin = session.get('loggedin')
    username = session.get('username')
    user_type = session.get('user_type')
    user_id = session.get('user_id')

    info = db.user_info_by_name(pname)

    if info is None:
        return redirect('/')
    
    posts = db.get_user_betslips(user_id, True)
    # return str(posts)

        
    return render_template('userpage.html', 
                            loggedin=loggedin,
                            username=username,
                            user_type=user_type,
                            info=info,
                            posts=posts)
    

# end of pages 
# start of functions

@app.route('/logout')
def logout_page():
    session.clear()
    return redirect('/')

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

 
    if validate_addition(selected, row, col, matches):
        return 'hmm thsis needs validation!'
    
    flag = False
    # Check if the clicked match is in the betslip
    for s in session['selected']:
            if selected_match['match_id'] == s['match_id']:
                flag = True
                swap = s
    # Replace the existing bet with the new one
    if flag:
        for i, item in enumerate(selected):
            if item == swap:
                selected[i] = selected_match
    # If it's a new match add it to selected list
    else:
        selected.append(selected_match)
    
    # update the selected bets in the sesion
    session['selected'] = selected
    

    return redirect_last()  

@app.route('/add_comment', methods=["GET", "POST"])
def add_comment():
    loggedin = session.get('loggedin')
    user_id = session.get('user_id')
    post_id = request.args.get('post_id')
    context = request.args.get('context')

    if loggedin is not None and post_id is not None:
        success = db.add_comment_to_post(user_id, int(post_id), context)

        return redirect_last()
    return redirect_last()

@app.route('/like_post', methods=["GET", "POST"])
def like_post():
    loggedin = session.get('loggedin')
    user_id = session.get('user_id')
    post_id = request.args.get('post_id')

    if loggedin is not None and post_id is not None:
        success = db.like_post(user_id, post_id)

        if success is False:
            db.get_like_back(user_id, post_id)

        return redirect_last()
    return redirect_last()

# end of functions