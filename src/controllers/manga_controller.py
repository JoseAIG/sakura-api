from flask import request
from database import db
from helpers.jwt_tools import authTokenRequired, decodeToken
from helpers.file_upload import uploadFiles
from models.manga import Manga


def getManga(id):
    try:
        manga = Manga.query.get(id)
        return {'status':200, 'manga_id':manga.id, 'user_id':manga.user_id, 'title':manga.title, 'description':manga.description, 'author':manga.author, 'status':manga.status, 'year':manga.year, 'chapters':manga.chapters, 'cover_image':manga.cover_image, 'date_created':manga.date_created.strftime("%d/%m/%Y")}, 200
    except Exception as e:
        print(e)
        return {'status':500, 'message':'Could not get manga'}, 500


@authTokenRequired
def createManga():
    try:
        title = request.form['title']
        description = request.form['description']
        author = request.form['author']
        status = request.form['status']
        year = request.form['year']
        chapters = request.form['chapters']
        coverURL = uploadFiles('cover', 'covers/')[0]

        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')

        newManga = Manga(userID, title, description, author, status, year, chapters, coverURL)
        db.session.add(newManga)
        db.session.commit()

        return {'status':200, 'message':'Manga created successfully'}, 200
    except Exception:
        return {'status':500, 'message':'Could not create manga'}, 500