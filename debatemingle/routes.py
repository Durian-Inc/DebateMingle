from debatemingle.utils import *
from random import random, randrange
from json import dumps
from linecache import getline
from debatemingle import app, socketio
from flask import render_template, request, render_template, flash, redirect
from flask import session as browser_session
from flask_socketio import disconnect

app.secret_key = 'thats-tru-man'

silly_queue = []
serious_queue = []

chats = {}


def chat_handler(room):
    def handler(contents):
        socketio.send(contents, room=room)
    return handler


def get_opinions():
    opinions = ['👍', '👎']
    if random() > 0.5:
        opinions[0], opinions[1] = opinions[1], opinions[0]
    return opinions


def random_topic():
    thing = getline('./debatemingle/static/data/silly.csv', randrange(20))
    return thing[:-1]


def serious_topic():
    thing = getline('./debatemingle/static/data/silly.csv', randrange(10))
    return thing[:-1]


def setup_chat():
    id1 = silly_queue.pop(0)
    id2 = silly_queue.pop(0)
    chats[id1] = id2
    chats[id2] = id1
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


def serious_chat():
    id1 = serious_queue.pop(0)
    id2 = serious_queue.pop(0)
    chats[id1] = id2
    chats[id2] = id1
    topic = serious_topic()
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


def check_length():
    if len(silly_queue) > 1:
        setup_chat()
    if len(serious_queue) > 1:
        serious_chat()


@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    print("reached disconnect")
    if sid in chats:
        print("disconnecting")
        disconnect(chats[sid])
        del chats[chats[sid]]
        del chats[sid]
    if sid in silly_queue:
        del silly_queue[silly_queue.index(sid)]


@socketio.on('okay')
def handle_okay(message):
    if message == 'zany':
        silly_queue.append(request.sid)
    else:
        serious_queue.append(request.sid)
    check_length()


@socketio.on('msg')
def handle_msg(contents):
    recipient = chats[request.sid]
    socketio.emit('msg', data=contents, room=recipient)


@app.route('/')
@login_required
def index():
    db.create_all()
    return render_template("zany.html")


@app.route('/serious', methods=['GET', 'POST'])
@login_required
def serious():
    if request.method == 'GET':
        return render_template("serious.html", topic=random_topic())


@app.route('/topics', methods=['GET', 'POST'])
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
            if add_user(check_username, check_passhash):
                flash("Your account does not exist, creating one now!")
                browser_session['username'] = check_username
                return redirect('/', code=302)
            else:
                flash("Wrong credentials")
    return redirect('/', code=302)


@app.route('/logout/', methods=['GET'])
@login_required
def signout():
    browser_session.pop("username")
    flash("Signed out successfully!")
    return redirect("/", code=302)
