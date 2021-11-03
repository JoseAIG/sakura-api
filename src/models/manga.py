from database import db
from datetime import datetime, timedelta

class Manga(db.Model):
    __tablename__ = 'mangas'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    author = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(15), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    chapters = db.Column(db.Integer, nullable=True)
    cover_image = db.Column(db.String(255), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow()-timedelta(hours=4))
    manga_chapters = db.relationship('Chapter', cascade="all, delete", backref="manga")

    # CONSTRUCTOR
    def __init__(self, user_id, title, description, author, status, year, chapters, cover_image):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.author = author
        self.status = status
        self.year = year
        self.chapters = chapters
        self.cover_image = cover_image