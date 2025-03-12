from app import db
from app.config import Config as c

class FlagsModel(db.Model):
    flag_id = db.Column("flag_id", db.Integer, primary_key=True, autoincrement=True)
    level = db.Column("username", db.Integer, unique=True)
    flag = db.Column("flag", db.String(128))
    
class Level1Model(db.Model):
    user_id = db.Column("user_id", db.Integer, primary_key=True, autoincrement=True)
    username = db.Column("username", db.String(128), unique=True)
    hashed_password = db.Column("hashed_password", db.String(128))

    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password

class Level3Model(db.Model):
    comment_id = db.Column("comment_id", db.Integer, primary_key=True, autoincrement=True)
    comment_content = db.Column("comment_content", db.String(1024))

    def __init__(self, comment_content):
        self.comment_content = comment_content

class CookieModel(db.Model):
    cookie_id = db.Column("pin_id", db.Integer, primary_key=True, autoincrement=True)
    cookie_key = db.Column("cookie_key", db.String(c.SECRET_COOKIE_KEY_LEN))
    cookie_value = db.Column("cookie_value", db.String(c.SECRET_COOKIE_VALUE_LEN))

class Level4Model(db.Model):
    pin_id = db.Column("pin_id", db.Integer, primary_key=True, autoincrement=True)
    pin = db.Column("pin", db.String(16))

class Level5Model(db.Model):
    pin_id = db.Column("pin_id", db.Integer, primary_key=True, autoincrement=True)
    pin = db.Column("pin", db.String(16))

    def __init__(self, pin):
        self.pin = pin
