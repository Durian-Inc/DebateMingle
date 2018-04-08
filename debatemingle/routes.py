from random import random, randrange
from json import dumps
from linecache import getline
import threading
from debatemingle import app, socketio
from flask import Blueprint, render_template, request, render_template, flash, redirect
from flask import session as browser_session
from debatemingle.utils import *

users = []

def chat_handler(room):
    print("CREATING", room)
    def handler(contents):
        print("SENDING", contents, "TO", room)
        room.emit('msg', contents)
        # socketio.send(contents, room=room)
    return handler


def get_opinions():
    opinions = ['👍', '👎']
    if random() > 0.5:
        opinions[0], opinions[1] = opinions[1], opinions[0]
    return opinions


def random_topic():
    thing = getline('./debatemingle/static/data/silly.csv', randrange(20))
    return thing[:-1]


def setup_chat():
    id1 = users.pop(0)
    print("ID1", id1)
    id2 = users.pop(0)
    print("ID2", id2)
    handle1 = chat_handler(id1)
    handle2 = chat_handler(id2)
    socketio.on_event('msg', handle1, namespace=id2)
    socketio.on_event('msg', handle2, namespace=id1)
    topic = random_topic()
    opinions = get_opinions()
    socketio.emit('okay', {
        'name': 'Jeff',
        'topic': topic,
        'opinion': opinions[0]
    }, room=id1)
    socketio.emit('okay', {
        'name': 'Wangus',
        'topic': topic,
        'opinion': opinions[1]
    }, room=id2)
    print('done')


def check_length():
    if len(users) > 1:
        setup_chat()
    t = threading.Timer(1, check_length)
    t.start()


@socketio.on('connect')
def handle_connect():
    users.append(request.sid)
    check_length()


@socketio.on('okay')
def handle_okay(message):
    print("Recived {} from {}".format(message, request.sid))

app.secret_key = 'thats-tru-man'

@app.route('/')
def index():
    db.create_all()
    print(get_all_users())
    return render_template("zany.html")


@app.route('/serious', methods = ['GET','POST'])
def serious():
    if request.method == 'GET':
        return render_template("serious.html", topic = random_topic())


@app.route('/topics', methods = ['GET', 'POST'])
def topics():
    if request.method == 'GET':
        topic_list = [line[0:-1] for line in open('./debatemingle/static/data/silly.csv', "r").readlines()]
        return dumps(topic_list)
            

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
            if add_user(request.form['username'], request.form['password']):
                print("Good")
                return redirect('/', code=302)
            else:
                print ("That username is taken")
    return redirect('/', code=302)
    
@app.route('/logout/', methods=['GET'])
def signout():
    browser_session.pop("username")
    flash("Signed out successfully!")
    return redirect("/", code=302)
