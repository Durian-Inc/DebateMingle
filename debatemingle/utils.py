from hashlib import sha256
from debatemingle.models import *
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
        hash_pass = sha256(password.encode('utf-8')).hexdigest()
        new_account = Account(username, hash_pass)
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

def check_user_interation(current_username, current_topic):
    """
    @purpose: Check if the given user has interacted with the topic in someway. 
    @args: The username of the current user. The topic in question
    @returns: True if the interation exists and false if it does not.
    """
    result = VotedOn.query.filter_by(person = current_username, topic = current_topic).first()
    if result:
        return True
    else:
        return False

def get_all_users():
    """
    @purpose: Get the usernames of all the users in the databaes
    @args: None
    @returns: A list of all the usernames
    """
    return [account.username for account in Account.query.all()]