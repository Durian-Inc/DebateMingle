from app import app
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://@localhost/debate'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Account(db.Model):
    """Account for each individual.

    Attributes:
        username: The user's unique username.
        password: The password that the user has entered but in a hashed form.
    """
    __tablename__ = "account"

    username = db.Column(db.String, nullable = False, unique = True, primary_key = True)
    password = db.Column(db.String , nullable = False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<Account %r>' % (self.username)

class Topic(db.Model):
    """Topics that are in the datanase. 

    Attributes:
        name: The unique name of the topic.
    """
    __tablename__ = "topic"

    name = db.Column(db.String(80), primary_key = True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Topic %r>' % (self.name)
        
class VotedOn(db.Model):
    """The correlation between the user and each topic they have interacted with.

    Attributes:
        person: The name of the person for a given entry.
        topic: The topic at hand.
        vote: The user's opinion of the topic. 
    """
    __tablename__ = "votedon"

    person = db.Column('person', db.String, db.ForeignKey('account.username'), primary_key = True)
    topic = db.Column('topic', db.String, db.ForeignKey('topic.name'), primary_key = True)
    vote = db.Column('vote', db.Integer, nullable = False)

    def __init__(self, person, topic, vote):
        self.person = person
        self.topic = topic
        self.vote = vote
    
    def __repr__(self):
        return '<Voted %r>' % (self.vote)
