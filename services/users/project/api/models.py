import time
import datetime
import os
from project import db, bcrypt


class User(db.Model):
    __tablename__ = 'tbl_account'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone_number = db.Column(db.String(16), nullable=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)

    def __init__(self, user_name, password, email, phone_number, first_name, last_name, status, is_admin, is_active):
        self.user_name = user_name
        self.password = bcrypt.generate_password_hash(
            password, os.getenv('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.email = email
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.status = status
        if is_active is None:
            self.is_active = False
        else:
            self.is_active = is_active
        self.registered_on = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        if is_admin is None:
            self.is_admin = False
        else:
            self.is_admin = is_admin

    def to_json(self):
        return {
            'id': self.id,
            'username': self.user_name,
            'email': self.email,
            'active': self.is_active,
            'admin': self.is_admin,
            'phone_number': self.phone_number,
            'last_login': self.last_login,
            'first_name':self.first_name,
            'last_name':self.last_name,
        }


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
