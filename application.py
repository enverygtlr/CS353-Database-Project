from flask import * 
from flask_bootstrap import Bootstrap
import database as db
from util import redirect_last


app = Flask(__name__)
boot = Bootstrap(app)

app.secret_key = '9c543e044e10b6e0bfb7'

# start of pages
@app.route('/')
def home_page():
    loggedin = session.get('loggedin') # True if exists else None
    matches = db.all_matches()


    return render_template('homepage.html', 
                            loggedin=True,
                            matches=matches)

@app.route('/login')
def login_page():
    return render_template('base.html', 
                            loggedin=None)

@app.route('/register')
def register_page():
    return render_template('base.html', 
                            loggedin=True)

@app.route('/logout')
def logout_page():
    session.clear()
    
    return redirect_last()

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

@app.route('/remove_selected_bet', methods=["GET", "POST"])
def remove_selected_bet():
    return ''
