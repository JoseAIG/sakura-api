from database import db
from datetime import datetime, timedelta

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    edited = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow()-timedelta(hours=4))
    replies = db.relationship('Reply', cascade="all, delete", backref="comment")

    #CONSTRUCTOR
    def __init__(self, user_id, chapter_id, content ):
        self.user_id = user_id
        self.chapter_id =  chapter_id
        self.content = content

class Reply(db.Model):
    __tablename__ = "replies"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    edited = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow()-timedelta(hours=4))

    #CONSTRUCTOR
    def __init__(self, user_id, comment_id, content ):
        self.user_id = user_id
        self.comment_id =  comment_id
        self.content = content