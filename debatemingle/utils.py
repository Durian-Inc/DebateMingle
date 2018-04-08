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
    hash_pass = sha256(password.encode('utf-8')).hexdigest()
    new_account = Account(username, hash_pass)
    db.session.add(new_account)
    db.session.commit()
    print("Added the new user %s" %username)


def add_response(username, topic, response):
    """
    @purpose: Add a user's response to the database.
    @args: The user's unique ID number. The topic that has a new response. The user's response
    @return: None
    """
    new_vote = VotedOn(username, topic, response)
    models.db.session.add(new_vote)
    models.db.commit()
