from debatemingle import app, socketio
from debatemingle.utils import get_hash, auth_user
from flask import Blueprint, render_template, request, render_template, session, flash, redirect

app.secret_key = 'thats-tru-man'

@socketio.on('okay')
def handle_okay(message):
    print(message)

@app.route('/')
def index():
    return render_template("zany.html")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        check_username = request.form['username']
        check_passhash = get_hash(request.form['password'])
        if auth_user(check_username, check_passhash) is not None:
            session['username'] = check_username
            flash("Successfully logged in, " + session['username'])
        else:
            flash("Failed to log in, try again!")
    return redirect('/', code=302)


@app.route('/logout/', methods=['GET'])
def signout():
    session.pop("username")
    flash("Signed out successfully!")
    return redirect("/", code=302)
