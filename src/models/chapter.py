from database import db
from datetime import datetime, timedelta

class Chapter(db.Model):
    __tablename__ = "chapters"
    id = db.Column(db.Integer, primary_key=True)
    manga_id = db.Column(db.Integer, db.ForeignKey('mangas.id'))
    number = db.Column(db.Integer, nullable=False)
    chapter_images = db.Column(db.ARRAY(db.String(255)), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow()-timedelta(hours=4))
    comments = db.relationship('Comment', cascade="all, delete", backref="chapter")

    #CONSTRUCTOR
    def __init__(self, manga_id, number, chapter_images ):
        self.manga_id = manga_id
        self.number =  number
        self.chapter_images = chapter_images