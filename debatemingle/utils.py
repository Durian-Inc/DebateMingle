from hashlib import sha256
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://@localhost/debate'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

def get_hash(password):
    return sha256(password.encode('utf-8')).hexdigest()


def auth_user(username, hashed_password=None):
    return True

def add_user(new_account):
    db.session.add(new_account);
    db.session.commit()
