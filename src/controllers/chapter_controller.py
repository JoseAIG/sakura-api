from flask import request
from database import db
from helpers.jwt_tools import authTokenRequired, decodeToken
from helpers.file_upload import uploadFiles
from helpers.notifications import sendNotifications
from models.manga import Manga
from models.chapter import Chapter
from models.user import User
from s3 import deleteDirectory

#Getting the chapter info for reading
def getChapter(mangaID, number):
    try:
        #Query the chapter info using the identifier provided
        chapter = Chapter.query.filter_by(manga_id=mangaID, number=number).first()
        if(chapter is None):
            return {'status':400, 'message':'Chapter does not exist'},400
        return {'status':200, 'chapter_id':chapter.id, 'manga_id':chapter.manga_id, 'number':chapter.number, 'chapter_images':chapter.chapter_images, 'date_created':chapter.date_created.strftime("%d/%m/%Y")},200
    except Exception as e:
        print(e)
        return {'status':500, 'message':'Could not get Chapter'},500
    
#Getting all manga chapters using the manga id
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
def createChapter(mangaID):
    try:
        # GET USER FROM ITS ID STORED IN PROVIDED TOKEN
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)
        # GET MANGA FROM PROVIDED MANGA ID 
        manga = Manga.query.get(mangaID)
        if(manga is not None):
            if(user.admin or manga.user_id == user.id):
                # CHECK IF CHAPTER ALREADY EXISTS IN MANGA
                number = request.form['number']
                chapter = Chapter.query.filter_by(manga_id=mangaID, number=number).first()
                if(chapter is not None):
                    return {'status':409, 'message':'Chapter already exists in this manga'},409
                else:
                    chapterImagesURL = uploadFiles('images[]','chapters/'+mangaID+'/'+number+'/')

                    newChapter = Chapter(mangaID, number, chapterImagesURL)
                    db.session.add(newChapter)
                    db.session.commit()
                    
                    # SEND NOTIFICATION TO USERS
                    users = User.query.filter(User.followed_mangas.any(int(mangaID))).all()
                    notificationTokens = []
                    for user in users:
                        if(user.notification_token):
                            notificationTokens.append(user.notification_token)
                    
                    sendNotifications(
                        "New chapter released!",
                        "Good news, {0} has a new chapter ({1})".format(manga.title, number),
                        notificationTokens,
                        {"mangaID": mangaID}
                    )

                    return {'status':200, 'message':'Chapter uploaded successfully'},200
            else:
                return {'status':403, 'message':'You do not have permissions for creating this chapter'},403
        else:
            return {'status':400, 'message':'Manga does not exist, cannot upload chapter'},400

    except Exception as e:
        print(e)
        return {'status':500, 'message':'Could not upload chapter'},500

@authTokenRequired
def updateChapter(mangaID, number):
    try:
        chapter = Chapter.query.filter_by(manga_id=mangaID, number=number).first()
        #If chapter exists, chapter deletion continues
        if(chapter is None):
            return {'status':400, 'message':'Chapter does not exist'},400
        else:
            changeFlag = False
            if(chapter.number != int(request.form['number'])):
                chapterNumber = Chapter.query.filter_by(manga_id=mangaID, number=request.form['number']).first()
                if(chapterNumber is None ):
                    chapter.number = request.form['number']
                    changeFlag = True
                else:
                    return {'status':409, 'message':'Chapter already exists in this manga'},409
            if not request.files['images[]'].filename == '':
                deleteDirectory('chapters/'+mangaID+'/'+number+'/')
                chapter.chapter_images = uploadFiles('images[]','chapters/'+mangaID+'/'+number+'/')
                changeFlag = True
            #Commit if changes were made
            if changeFlag:
                db.session.commit()
                return {'status':200, 'message': 'Chapter successfully edited'}, 200
            else:
                return {'status':400, 'message':'Data provided is same as current'}, 400
    except Exception:
        return {'status':500, 'message':'Could not update Chapter'}, 500

@authTokenRequired
def deleteChapter(mangaID, number):
    try:
        # GET USER FROM ITS ID STORED IN PROVIDED TOKEN
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)
        # GET MANGA FROM PROVIDED MANGA ID 
        manga = Manga.query.get(mangaID)
        # CHECK IF USER CAN DELETE THE CHAPTER
        if(user.admin or manga.user_id == user.id):
            # GET CHAPTER FROM PROVIDED CHAPTER ID
            chapter = Chapter.query.filter_by(manga_id=mangaID, number=number).first()
            if(chapter is None):
                return {'status':400, 'message':'Chapter does not exist'},400
            else:
                deleteDirectory('chapters/'+mangaID+'/'+number+'/')
                db.session.delete(chapter)
                db.session.commit()
                return {'status':200, 'message':'Chapter successfully deleted'}, 200
        else:
            return {'status':403, 'message':'You do not have permissions for deleting this chapter'},403

    except Exception as e:
        print(e)
        return {'status':500, 'message':'Could not delete chapter'}, 500