from debatemingle import app
from debatemingle.utils import get_hash, auth_user
from flask import Blueprint, render_template, request, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import session as browser_session
from debatemingle import models

app.secret_key = 'thats-tru-man'

@app.route('/')
def index():
    db.create_all()
    account = Account(name="Bobby", password="Hill")
    db.session.add(account)
    db.session.commit()
    return render_template("zany.html")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        db.create_all()
        check_username = request.form['username']
        check_passhash = get_hash(request.form['password'])
        account = Account(request.form['username'], request.form['password'])
        db.session.add(account)
        db.session.commit()
        if auth_user(check_username, check_passhash) is not None:
            browser_session['username'] = check_username
            flash("Successfully logged in, " + browser_session['username'])
        else:
            flash("Your account does not exist, creating one now!")
    return redirect('/', code=302)


@app.route('/logout/', methods=['GET'])
def signout():
    browser_session.pop("username")
    flash("Signed out successfully!")
    return redirect("/", code=302)
