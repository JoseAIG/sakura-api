from flask import request
from database import db
from helpers.jwt_tools import authTokenRequired, decodeToken
from helpers.file_upload import uploadFiles
from s3 import deleteFile
from models.manga import Manga
from models.chapter import Chapter

#Getting the chapter info for reading
def getChapter(chapterID):
    try:
        #Query the chapter info using the identifier provided
        chapter = Chapter.query.get(chapterID)
        return {'status':200, 'chapter_id':chapter.id, 'manga_id':chapter.manga_id, 'number':chapter.number, 'chapter_images':chapter.chapter_images, 'date_created':chapter.date_created.strftime("%d/%m/%Y")},200
    except Exception as e:
        print(e)
        return {'status':500, 'message':'Could not get Chapter'},500
    
#Getting all mangas chapters using the mangaID
def getMangaChapters(mangaID):
    try:
        #Query the chapters using the provided ID
        mangaChapters = Chapter.query.filter_by(manga_id = mangaID).order_by(Chapter.id.desc()).all()
        #Generating the chapter list for the specific manga
        mangaChapterList = []
        for chapter in mangaChapters:
            chapterData = {'status':200, 'chapter_id':chapter.id, 'manga_id':chapter.manga_id, 'number':chapter.number, 'chapter_images':chapter.chapter_images, 'date_created':chapter.date_created.strftime("%d/%m/%Y")}
            mangaChapterList.append(chapterData)
        return {'status':200, 'manga_chapters':mangaChapterList},200
    except Exception as e:
        print(e)
        return{'status':500,'message':'Could not get manga chapters'}

@authTokenRequired
def createChapter():
    try:
        mangaID = request.form['mangaID']
        manga = Manga.query.get(mangaID)
        #If manga exists, chapter upload continues
        if(manga is None):
            return {'status':400, 'message':'Manga does not exist, cannot upload chapter'},400
        else:
            number = request.form['number']
            chapterImagesURL = uploadFiles('chapterImages[]','chapters/'+mangaID)

            newChapter = Chapter(mangaID,number,chapterImagesURL)
            db.session.add(newChapter)
            db.session.commit()

            return {'status':200, 'message':'Chapter uploaded successfully'},200

    except Exception:
        return {'status':500, 'message':'Could not upload chapter'},500

@authTokenRequired
def updateChapter():
    try:
        mangaID = request.form['mangaID']
        chapterID = request.form['id']
        chapter = Chapter.query.get(chapterID)
        #If chapter exists, chapter deletion continues
        if(chapter is None):
            return {'status':400, 'message':'Chapter does not exist'},400
        else:
            changeFlag = False
            if(chapter.number != request.form['number']):
                chapter.number = request.form['number']
                changeFlag = True
            if not request.files['chapterImages[]'].filename == '':
                chapter.chapter_images = uploadFiles('chapterImages[]','chapters/'+mangaID)
                changeFlag = True
            #Commit if changes were made
            if changeFlag:
                db.session.commit()
                return {'status':200, 'message': 'Chapter successfully edited'}, 200
    except Exception:
        return {'status':500, 'message':'Could not update Chapter'}, 500

@authTokenRequired
def deleteChapter():
    try:
        mangaID = request.form['mangaID']
        chapterID = request.form['id']
        chapter = Chapter.query.get(chapterID)
        #If chapter exists, chapter deletion continues
        if(chapter is None):
            return {'status':400, 'message':'Chapter does not exist'},400
        else:
            #deleteFiles("chapters"+mangaID,'param')
            db.session.delete(chapter)
            db.session.commit()
            return {'status':200, 'message':'Chapter successfully deleted'}, 200
    except Exception:
        return {'status':500, 'message':'Could not delete chapter'}, 500