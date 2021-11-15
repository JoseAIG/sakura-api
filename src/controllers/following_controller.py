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
        # GETTING THE USER INFO 
        userData = User.query.get(userID)
        # NOW GETTING THE FOLLOWED ONES
        followedMangas = userData.followed_mangas
        
        return {'status':200, 'followed_mangas': followedMangas}, 200
    
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

        followedMangas = user.followed_mangas

        for followed in followedMangas:
            if(followed == mangaID):
                return {'status':400, 'message':'Already following this manga'},400
            else:
                followedMangas.append(mangaID)
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

        followedMangas = user.followed_mangas

        for followed in followedMangas:
            if(followed != mangaID):
                return {'status':400, 'message':'Not following this manga'},400
            else:
                index = indexOf(followed)
                del followedMangas[index]
                db.session.commit()
                return {'status':200, 'message':'Manga successfully unfollowed'}, 200
    
    except Exception as e:
        print(e)
        return {'status':500, 'message':'Could not unfollow manga'}