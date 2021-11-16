import bcrypt
from flask import request
from database import db
from models.user import User
from models.manga import Manga
from helpers.jwt_tools import authTokenRequired, decodeToken, generateToken
from s3 import deleteDirectory, deleteFile

@authTokenRequired
def getUser():
    try:
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)
        return {'status': 200, 'username': user.username, 'email': user.email, 'date_created': user.date_created.strftime("%d/%m/%Y")}, 200
    except Exception as e:
        return {'status': 500, 'message':'Could not get user data'}, 500

@authTokenRequired
def updateUser():
    try:
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)
        changeFlag = False
        if user.username != request.form['username']:
            user.username = request.form['username']
            changeFlag = True
        if user.email != request.form['email']:
            user.email = request.form['email']
            changeFlag = True
        if request.form['password'] != "":
            user.password = bcrypt.hashpw(request.form['password'].encode('utf8'), bcrypt.gensalt()).decode()
            changeFlag = True
        # IF CHANGES WERE MADE, COMMIT CHANGES TO DB AND GENERATE A NEW TOKEN
        if changeFlag:
            db.session.commit()
            userToken = generateToken({'id':user.id, 'username':user.username, 'email':user.email, 'admin':user.admin})
            return {'status':200, 'message':'User updated successfully', 'token':userToken}, 200
        else:
            return {'status':400, 'message':'Data provided is same as current'}, 400
    except Exception as e:
        print(e)
        if('username' in e.args[0]):
            return {'status': 409, 'message': 'Username already registered'}, 409
        elif('email' in e.args[0]):
            return {'status': 409, 'message': 'e-mail already registered'}, 409
        else:
            return {'status': 500, 'message':'Could not update user data'}, 500

@authTokenRequired
def deleteUser():
    try:
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)

        # GET USER MANGAS AND REMOVE FILES FROM S3
        mangas = Manga.query.filter_by(user_id=userID).all()
        for manga in mangas:
            deleteFile("covers/", manga.cover_image)
            deleteDirectory("chapters/"+str(manga.id)+"/")

        db.session.delete(user)
        db.session.commit()
        return {'status':200, 'message':'User deleted successfully'}, 200
    except Exception as e:
        print(e)
        return {'status':500, 'message':"Could not delete user"}, 500

@authTokenRequired
def storeNotificationToken():
    try:
        # GET USER FROM USER'S JWT
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)

        # SET USER'S NOTIFICATION TOKEN
        user.notification_token = request.json['value']
        db.session.commit()

        return {'status':200, 'message':'Token successfully stored'}, 200
    except Exception:
        return {'status':500, 'message':"Could not store notification token"}, 500