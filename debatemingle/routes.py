from debatemingle import app
from debatemingle.utils import get_hash, auth_user
from flask import Blueprint, render_template, request, render_template, flash, redirect
from flask import session as browser_session
from debatemingle import models, utils


app.secret_key = 'thats-tru-man'

@app.route('/')
def index():
    models.db.create_all()
    return render_template("zany.html")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        check_username = request.form['username']
        check_passhash = get_hash(request.form['password'])
        if auth_user(check_username, check_passhash) is True:
            browser_session['username'] = check_username
            flash("Successfully logged in, " + browser_session['username'])
        else:
            flash("Your account does not exist, creating one now!")
            utils.add_user(request.form['username'], request.form['password'])
    return redirect('/', code=302)


@app.route('/logout/', methods=['GET'])
def signout():
    browser_session.pop("username")
    flash("Signed out successfully!")
    return redirect("/", code=302)
