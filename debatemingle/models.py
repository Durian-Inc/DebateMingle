from debatemingle import db
class Account(db.Model):
    
    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False, unique = True)
    password = db.Column(db.String(80) , nullable = False)

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<Account %r>' % (self.id)

class Topic(db.Model):
    
    __tablename__ = "topic"
    name = db.Column(db.String(80), primary_key = True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Topic %r>' % (self.name)
        
class VotedOn(db.Model):
    
    __tablename__ = "votedon"
    person = db.Column('person', db.Integer, db.ForeignKey('account.id'), primary_key = True)
    topic = db.Column('topic', db.String, db.ForeignKey('topic.name'), primary_key = True)
    vote = db.Column('vote', db.Integer, primary_key = True)

    def __init__(self, person, topic, vote):
        self.person = person
        self.topic = topic
        self.vote = vote
    
    def __repr__(self):
        return '<Voted %r>' % (self.vote)