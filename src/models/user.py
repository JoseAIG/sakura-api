from database import db
from datetime import datetime, timedelta

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False, unique=True)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(65), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow()-timedelta(hours=4))
    mangas = db.relationship('Manga', cascade="all, delete", backref="usuario")

    # CONSTRUCTOR
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password