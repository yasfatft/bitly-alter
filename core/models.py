from sqlalchemy.orm import relationship
from flask_serialize import FlaskSerializeMixin

from core.app import db
from core.config import LONG_URL_MAX_LENGTH


def add_to_database(object):
    db.session.add(object)
    db.session.commit()


class User(db.Model, FlaskSerializeMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String())
    authenticated = db.Column(db.Boolean, default=False)

    list_urls = db.relationship('Url',
                                backref=db.backref("owner"),
                                lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the id to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def __repr__(self):
        return '<User %r>' % (self.email)


class Url(db.Model, FlaskSerializeMixin):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(LONG_URL_MAX_LENGTH))
    short_url = db.Column(db.String(40))
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    db.UniqueConstraint('short_url', 'owner_id', name='uix_1')

    def __init__(self, long_url, short_url, owner_id):
        self.long_url = long_url
        self.short_url = short_url
        self.owner_id = owner_id

    def __repr__(self):
        return '<Url %r>' % (self.short_url + ", " + self.long_url)

    def __str__(self):
        return f'short_url: {self.short_url}, long_url: {self.long_url}'
