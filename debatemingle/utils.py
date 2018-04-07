from hashlib import sha256


def get_hash(password):
    return sha256(password.encode('utf-8')).hexdigest()


def auth_user(username, hashed_password=None):
    return True
