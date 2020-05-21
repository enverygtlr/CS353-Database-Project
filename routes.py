from flask import render_template, request, flash, Markup, redirect, url_for
from forms import RegistrationForm, LoginForm
from lib.config import *
from lib import database as db
import util
import olddb
from app import app


@app.route('/')
def home():
    matches = db.get_bet_table()
    return render_template('home.html', matches = matches)

@app.route('/adminpanel', methods=['GET', 'POST'])
def adminpanel():
    matches = db.get_bet_table()
    return render_template('adminpanel.html', matches = matches)

@app.route('/adminlogin', methods=['POST', 'GET'])
def adminlogin():
    form = LoginForm()
    if form.validate_on_submit():
        exists = db.login_check(form.email.data, form.password.data)
        if exists[0]['exists'] is True:
            flash('Succesfuly logged in!', 'success')
            #name = db.get_name_id(form.email.data)
            #name = name[0]['s_name']
            return redirect(url_for('adminpanel'))
        else:
            flash('Wrong username or password, please try again!', 'warning')
            return render_template('adminlogin.html', form = form )
    return render_template('adminlogin.html',  form=form )


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        exists = db.login_check(form.email.data, form.password.data)
        if exists[0]['exists'] is True:
            flash('Succesfuly logged in!', 'success')
            dbobject = db.get_name_id(form.email.data)
            name, id = name, id = dbobject[0]['s_name'], dbobject[0]['id']
            return redirect(url_for('hg', name=name))
        else:
            flash('Wrong username or password, please try again!', 'warning')
            return render_template('login.html', form = form )
    return render_template('login.html',  form=form )

@app.route('/hg')
def hg():
    return render_template('hg.html' )


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print('emaile giren: ==', form.email.data)
        exists = db.register_check(form.email.data)
        if exists[0]['exists'] is True:
            flash('Email is already taken, please try a different email!', 'danger')
            return redirect(url_for('register'))
        else:
            print("user added to db")
            flash('User created!', 'success')
            db.create_user(form.fullname.data, form.password.data, form.email.data)
        #exists = db.register_check(form.email.data)
        # print(exists[0]['exists'])
        # if exists[0]['exists'] is True:        
        #     flash('Email is already taken, try a different email!', 'danger')
        #     return redirect(url_for('register'))
        # else:
        #     #add to db
        #     print('account created successfuly')
        #     return redirect(url_for('hg'))

        return redirect(url_for('hg'))
    return render_template('register.html', form=form)
