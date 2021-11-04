from flask import request
from database import db
from helpers.jwt_tools import authTokenRequired, decodeToken
from helpers.file_upload import uploadFiles
from s3 import deleteFile, deleteDirectory
from models.manga import Manga
from models.user import User


def getManga(id):
    try:
        manga = Manga.query.get(id)
        if(manga is None):
            return {'status':400, 'message':'Manga does not exist'}, 400
        else:
            mangaChapters = []
            for chapter in manga.chapters:
                chapterData = {'id':chapter.id, 'manga_id':chapter.manga_id, 'number':chapter.number, 'chapter_images':chapter.chapter_images, 'date_created':chapter.date_created.strftime("%d/%m/%Y")}
                mangaChapters.append(chapterData)
            return {'status':200, 'manga_id':manga.id, 'user_id':manga.user_id, 'title':manga.title, 'description':manga.description, 'author':manga.author, 'status':manga.status, 'year':manga.year, 'cover_image':manga.cover_image, 'date_created':manga.date_created.strftime("%d/%m/%Y"), 'chapters':mangaChapters}, 200
    except Exception as e:
        print(e)
        return {'status':500, 'message':'Could not get manga'}, 500

@authTokenRequired
def getUserMangas():
    try:
        # GET USER'S ID FROM TOKEN
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        # QUERY MANGAS WITH USER'S ID
        userMangas = Manga.query.filter_by(user_id = userID).order_by(Manga.id.desc()).all()
        # ITERATE USER MANGAS GENERATING A LIST FOR PROVIDING THE RESPONSE
        userMangaList = []
        for manga in userMangas:
            # POPULATE MANGA CHAPTERS
            mangaChapters = []
            for chapter in manga.chapters:
                chapterData = {'id':chapter.id, 'manga_id':chapter.manga_id, 'number':chapter.number, 'chapter_images':chapter.chapter_images, 'date_created':chapter.date_created.strftime("%d/%m/%Y")}
                mangaChapters.append(chapterData)
            # POPULATE MANGA DATA
            mangaData = {'manga_id':manga.id, 'user_id':manga.user_id, 'title':manga.title, 'description':manga.description, 'author':manga.author, 'status':manga.status, 'year':manga.year, 'chapters':mangaChapters, 'cover_image':manga.cover_image, 'date_created':manga.date_created.strftime("%d/%m/%Y")}
            userMangaList.append(mangaData)
        return {'status':200, 'user_mangas': userMangaList}, 200
    except Exception as e:
        print(e)
        return {'status':500, 'message':'Could not get user mangas'}, 500

@authTokenRequired
def createManga():
    try:
        title = request.form['title']
        description = request.form['description']
        author = request.form['author']
        status = request.form['status']
        year = request.form['year']
        coverURL = uploadFiles('cover', 'covers/')[0]

        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')

        newManga = Manga(userID, title, description, author, status, year, coverURL)
        db.session.add(newManga)
        db.session.commit()

        return {'status':200, 'message':'Manga created successfully'}, 200
    except Exception as e:
        print(e)
        return {'status':500, 'message':'Could not create manga'}, 500

@authTokenRequired
def updateManga():
    try:
        # GET USER FROM ITS ID STORED IN PROVIDED TOKEN
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)
        # GET MANGA FROM PROVIDED ID
        mangaID = request.form['id']
        manga = Manga.query.get(mangaID)
        # CHECK IF MANGA EXISTS
        if(manga is None):
            return {'status':400, 'message':'Manga does not exist'}, 400
        # CHECK IF USER CAN EDIT THE MANGA
        if(user.admin or manga.user_id == userID):
            changeFlag = False
            if(manga.title != request.form['title']):
                manga.title = request.form['title']
                changeFlag = True
            if(manga.description != request.form['description']):
                manga.description = request.form['description']
                changeFlag = True
            if(manga.author != request.form['author']):
                manga.author = request.form['author']
                changeFlag = True
            if(manga.status != request.form['status']):
                manga.status = request.form['status']
                changeFlag = True
            if(manga.year != int(request.form['year'])):
                manga.year = request.form['year']
                changeFlag = True
            if not request.files['cover'].filename == '':
                deleteFile("covers/", manga.cover_image)
                manga.cover_image = uploadFiles('cover', 'covers/')[0]
                changeFlag = True
            # IF CHANGES WERE MADE, COMMIT THEM TO THE DB
            if changeFlag:
                db.session.commit()
                return {'status':200, 'message':'Manga successfully edited'}, 200
            else:
                return {'status':400, 'message':'Data provided is same as current'}, 400
        else:
            return {'status':403, 'message':'You can not edit this manga'}, 403
    except Exception as e:
        print(e)
        return {'status':500, 'message':'Could not update manga'}, 500

@authTokenRequired
def deleteManga(id):
    try:
        # GET USER FROM ITS ID STORED IN PROVIDED TOKEN
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)
        # GET MANGA FROM PROVIDED ID
        manga = Manga.query.get(id)
        # CHECK IF MANGA EXISTS
        if(manga is None):
            return {'status':400, 'message':'Manga does not exist'}, 400
        # CHECK IF USER CAN EDIT THE MANGA
        if(user.admin or manga.user_id == userID):
            deleteFile("covers/", manga.cover_image)
            deleteDirectory("chapters/"+id+"/")
            db.session.delete(manga)
            db.session.commit()
            return {'status':200, 'message':'Manga successfully deleted'}, 200
        else:
            return {'status':403, 'message':'You can not delete this manga'}, 403
    except Exception as e:
        print(e)
        return {'status':500, 'message':'Could not delete manga'}, 500
