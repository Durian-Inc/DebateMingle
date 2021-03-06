import csv
from json import dumps, loads
from linecache import getline
from random import choice, random

from flask import flash, redirect, render_template, request
from flask import session as browser_session
from flask_socketio import disconnect

from app import app, socketio
from app.utils import (add_response, add_user, auth_user,
                       check_user_interaction, get_all_users, get_hash,
                       login_required)

app.secret_key = 'thats-tru-man'

silly_queue = []
serious_queue = []

chats = {}
username = {}


def match_preferences():
    data = get_all_users()
    for player in data:
        player = loads(player)
        if player['username'] in username:
            for likes in player['likes']:
                for player2 in data:
                    player2 = loads(player2)
                    if player2['username'] in username:
                        for dislikes in player2['dislikes']:
                            if likes == dislikes:
                                serious_chat(player['username'],
                                             player2['username'], likes)


def get_opinions():
    opinions = ['yes', 'no']
    if random() > 0.5:
        opinions[0], opinions[1] = opinions[1], opinions[0]
    return opinions


def random_topic():
    with open('./app/static/data/silly.csv') as f:
        reader = csv.reader(f)
        chosen_row = choice(list(reader))[0]
        return chosen_row


def serious_topic():
    thing = getline('./debatemingle/static/data/silly.csv', randrange(10))
    return thing[:-1]


def setup_chat():
    id1 = silly_queue.pop(0)
    id2 = silly_queue.pop(0)
    chats[id1] = id2
    chats[id2] = id1
    # name1 = [key for key, value in username.items() if value == id1][0]
    # name2 = [key for key, value in username.items() if value == id2][0]
    name1 = "Jimbo"
    name2 = "Frank"
    topic = random_topic()
    opinions = get_opinions()
    socketio.emit(
        'okay', {
            'name': name1,
            'topic': topic,
            'opinion': opinions[0]
        },
        room=id1)
    socketio.emit(
        'okay', {
            'name': name2,
            'topic': topic,
            'opinion': opinions[1]
        },
        room=id2)


def serious_chat(user1, user2, topic):
    serious_queue.pop(0)
    serious_queue.pop(0)
    id1 = username[user1]
    id2 = username[user2]
    chats[id1] = id2
    chats[id2] = id1
    opinions = get_opinions()
    socketio.emit(
        'okay', {
            'name': user1,
            'topic': topic,
            'opinion': opinions[0]
        },
        room=id1)
    socketio.emit(
        'okay', {
            'name': user2,
            'topic': topic,
            'opinion': opinions[1]
        },
        room=id2)


def check_length():
    if len(silly_queue) > 1:
        setup_chat()
    if len(serious_queue) > 1:
        match_preferences()


@socketio.on('vote')
def handle_vote(contents):
    match_preferences()


@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in chats:
        disconnect(chats[sid])
        try:
            del chats[chats[sid]]
        except KeyError:
            pass
        try:
            del chats[sid]
        except KeyError:
            pass
    if sid in silly_queue:
        del silly_queue[silly_queue.index(sid)]
        if sid in serious_queue:
            del serious_queue[serious_queue.index(sid)]


@socketio.on('mode')
def handle_mode(message):
    if message == 'zany':
        silly_queue.append(request.sid)
    else:
        serious_queue.append(request.sid)
        # username[browser_session['username']] = request.sid

    check_length()


@socketio.on('msg')
def handle_msg(contents):
    recipient = chats[request.sid]
    socketio.emit('msg', data=contents, room=recipient)


# @login_required
@app.route('/')
def index():
    return render_template("zany.html")


@app.route('/serious', methods=['GET', 'POST'])
@login_required
def serious():
    index()
    if request.method == 'GET':
        return render_template("serious.html", topic=random_topic())


@app.route('/topics', methods=['GET', 'POST'])
def topics():
    if request.method == 'GET':
        topic_list = [
            line[0:-1] for line in open('./debatemingle/static/data/silly.csv',
                                        "r").readlines()
        ]
        return dumps(topic_list)


@app.route('/check_topic/<topic>', methods=['GET'])
@login_required
def check_topic(topic):
    return str(check_user_interaction(browser_session['username'], topic))


@app.route('/add_response/<username>/<topic>/<response>', methods=['GET'])
@login_required
def add_one(topic, response):
    return add_response(browser_session['username'], topic, response)


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
            else:
                flash("Wrong credentials")

            return redirect('/', code=302)


@app.route('/logout/', methods=['GET'])
@login_required
def signout():
    browser_session.pop("username")
    flash("Signed out successfully!")
    return redirect("/", code=302)
