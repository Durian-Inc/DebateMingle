from hashlib import sha256
from debatemingle.models import *
from functools import wraps
from flask import redirect, flash
from flask import session as browser_session

def get_hash(password):
    """
    @purpose: Hash a given password to make sure we have tip top security.
    @args: The pre-hashed password.
    @returns: The hashed password using sha256
    """
    return sha256(password.encode('utf-8')).hexdigest()

def auth_user(check_username, check_password=None):
    """
    @purpose: Authenticate a user with their username and their hashed password.
    @args: The user's username. The hashed password.
    @return: True or false if the user is validated
    """
    result = Account.query.filter_by(username=check_username).first() 
    if result is not None and result.password == check_password:
        return True
    else:
        return False
    return False


def add_user(username, password):
    """
    @purpose: Add a new user to the database.
    @args: The username of the person. The user's unhashed password
    @return: None
    """
    try: 
        new_account = Account(username, password)
        db.session.add(new_account)
        db.session.commit()
        return True
    except:
        return False


def add_response(username, topic, response):
    """
    @purpose: Add a user's response to the database.
    @args: The user's unique ID number. The topic that has a new response. The user's response
    @return: None
    """
    new_vote = VotedOn(username, topic, response)
    models.db.session.add(new_vote)
    models.db.commit()

def check_user_interaction(current_username, current_topic):
    """
    @purpose: Check if the given user has interacted with the topic in someway. 
    @args: The username of the current user. The topic in question
    @returns: True if the interation exists and false if it does not.
    """
    result = VotedOn.query.filter_by(person = current_username, topic = current_topic).first()
    if result:
        return result.vote
    else:
        return False

def get_all_users(check_username = None):
    """
    @purpose: Get the usernames of all the users in the databaes
    @args: None
    @returns: A list of all the usernames
    """
    if check_username is None:
        return [account.username for account in Account.query.all()]
    else:
        usernames = {
            "agree":[], 
            "disagree":[]
        }
        current_user_topics = VotedOn.query.filter_by(person = check_username).all()
        for topic in current_user_topics:
            print (topic.topic)
            for person in VotedOn.query.all():
                if person.person != check_username:
                    if person.vote == topic.vote:
                        usernames["agree"].append(person.person)
                    else:
                        usernames["disagree"].append(person.person)
            return topic.topic, usernames


def login_required(func):
    """Wrap a function to enforce user authentication."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' in browser_session:
            return func(*args, **kwargs)
        else:
            flash("You must be logged in to access that page.", 'danger')
            return redirect('/login')
    return wrapper
