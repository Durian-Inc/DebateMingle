from debatemingle import app
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://@localhost/debate'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Account(db.Model):
    
    __tablename__ = "account"

    username = db.Column(db.String, nullable = False, unique = True, primary_key = True)
    password = db.Column(db.String , nullable = False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):

        return '<Account %r>' % (self.username)

class Topic(db.Model):
    __tablename__ = "topic"

    name = db.Column(db.String(80), primary_key = True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Topic %r>' % (self.name)
        
class VotedOn(db.Model):
    __tablename__ = "votedon"
    person = db.Column('person', db.String, db.ForeignKey('account.username'), primary_key = True)
    topic = db.Column('topic', db.String, db.ForeignKey('topic.name'), primary_key = True)
    vote = db.Column('vote', db.Integer, primary_key = True)

    def __init__(self, person, topic, vote):
        self.person = person
        self.topic = topic
        self.vote = vote
    
    def __repr__(self):
        return '<Voted %r>' % (self.vote)