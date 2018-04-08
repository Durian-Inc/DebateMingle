from random import random, randrange
from linecache import getline
import threading
from debatemingle import app, socketio
from debatemingle.utils import get_hash, auth_user
from flask import Blueprint, render_template, request, render_template, session, flash, redirect

app.secret_key = 'thats-tru-man'

silly_queue = []

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
    print('Chat has been set up for 2 users')


def check_length():
    if len(silly_queue) > 1:
        setup_chat()


@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in chats:
        socketio.disconnect(chats[sid])
        del chats[chats[sid]]
        del chats[sid]
    if sid in silly_queue:
        del silly_queue[silly_queue.index(sid)]


@socketio.on('connect')
def handle_connect():
    silly_queue.append(request.sid)
    check_length()


@socketio.on('okay')
def handle_okay(message):
    print("Recived {} from {}".format(message, request.sid))


@socketio.on('msg')
def handle_msg(contents):
    recipient = chats[request.sid]
    socketio.emit('msg', data=contents, room=recipient)


@app.route('/')
def index():
    return render_template("zany.html")


@app.route('/serious')
def serious():
    return render_template("serious.html")


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
