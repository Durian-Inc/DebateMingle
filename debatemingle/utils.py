from hashlib import sha256
from debatemingle import models
def get_hash(password):
    return sha256(password.encode('utf-8')).hexdigest()

def auth_user(username, hashed_password=None):
    """
    @purpose: Authenticate a user with their username and their hashed password.
    @args: The user's username. The hashed password.
    @return: True or false if the user is validated
    """
    
    

def add_user(username, password):
    """
    @purpose: Add a new user to the database.
    @args: The username of the person. The user's unhashed password
    @return: None
    """
    hash_pass = sha256(password.encode('utf-8')).hexdigest()
    new_account = models.Account(username, hash_pass)
    models.db.session.add(new_account)
    models.db.session.commit()
    print("Added the new user %s" %username)


def add_response(userid, topic, response):
    """
    @purpose: Add a user's response to the database.
    @args: The user's unique ID number. The topic that has a new response. The user's response
    @return: None
    """
    new_vote = VotedOn(userid, topic, response)
    models.db.session.add(new_vote)
    models.db.commit()
