from operator import indexOf
from flask import request
from database import db
from models.manga import Manga
from models.user import User
from helpers.jwt_tools import authTokenRequired, decodeToken

#get followed mangas
@authTokenRequired
def getFollowedMangas():
    try:
        # GET USER FROM USER'S ID PROVIDED IN JWT PAYLOAD
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)

        followedMangasID = user.followed_mangas
        followedMangas = []
        
        for mangaID in followedMangasID:
            manga = Manga.query.get(mangaID)
            # GET MANGA CHAPTERS
            mangaChapters = []
            for chapter in manga.chapters:
                chapterData = {'id':chapter.id, 'manga_id':chapter.manga_id, 'number':chapter.number, 'chapter_images':chapter.chapter_images, 'date_created':chapter.date_created.strftime("%d/%m/%Y")}
                mangaChapters.append(chapterData)
            # BUILD MANGA DATA AND APPEND TO FOLLOWED MANGAS
            mangaData = {'manga_id':manga.id, 'user_id':manga.user_id, 'title':manga.title, 'description':manga.description, 'author':manga.author, 'status':manga.status, 'year':manga.year, 'cover_image':manga.cover_image, 'date_created':manga.date_created.strftime("%d/%m/%Y"), 'chapters':mangaChapters}
            followedMangas.append(mangaData)

        return {'status':200, 'followedMangas': followedMangas}, 200
    
    except Exception as e:
        print(e)
        return {'status':500, 'message':'Could not get followed mangas'},500

#subscribe or follow a Manga
@authTokenRequired
def followManga(mangaID):
    try:
        # GET USER FROM USER'S ID PROVIDED IN JWT PAYLOAD
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)

        # CHECK IF MANGA EXISTS
        manga = Manga.query.get(mangaID)
        if(manga is None):
            return {'status':400, 'message':'Manga does not exist'},400

        # CHECK IF USER ALREADY FOLLOWS THE MANGA
        followedMangas = user.followed_mangas.copy()
        if(int(mangaID) in followedMangas):
            return {'status':400, 'message':'Already following this manga'},400
        else:
            followedMangas.append(int(mangaID))
            user.followed_mangas = followedMangas
            db.session.commit()
            return {'status':200, 'message':'Now following this manga'}

    except Exception as e:
        print(e)
        return {'status':500, 'message':'Could not follow manga'}

#unfollow a manga method
@authTokenRequired
def unfollowManga(mangaID):
    try:
         # GET USER FROM USER'S ID PROVIDED IN JWT PAYLOAD
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)

        # CHECK IF MANGA EXISTS
        manga = Manga.query.get(mangaID)
        if(manga is None):
            return {'status':400, 'message':'Manga does not exist'},400

        # CHECK IF USER ALREADY FOLLOWS THE MANGA
        followedMangas = user.followed_mangas.copy()
        if(int(mangaID) not in followedMangas):
            return {'status':400, 'message':'You are not following this manga'},400
        else:
            followedMangas.remove(int(mangaID))
            user.followed_mangas = followedMangas
            db.session.commit()
            return {'status':200, 'message':'Manga successfully unfollowed'}, 200
    
    except Exception as e:
        print(e)
        return {'status':500, 'message':'Could not unfollow manga'}