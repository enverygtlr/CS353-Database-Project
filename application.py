from flask import * 
from flask_bootstrap import Bootstrap


app = Flask(__name__)
boot = Bootstrap(app)

app.secret_key = 'dev'

@app.route('/')
def home_page():
    return render_template('base.html', loggedin=True)

@app.route('/login')
def login_page():
    return render_template('base.html', loggedin=True)

@app.route('/register')
def register_page():
    return render_template('base.html', loggedin=True)

@app.route('/logout')
def logout_page():
    session.clear()
    
    if redirect.referrer is None:
        return redirect('/')
        
    return redirect(redirect.referrer)