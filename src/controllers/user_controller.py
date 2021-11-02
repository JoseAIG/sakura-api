import bcrypt
from flask import request
from database import db
from models.user import User
from helpers.jwt_tools import authTokenRequired, decodeToken, generateToken

@authTokenRequired
def getUser():
    try:
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)
        return {'status': 200, 'username': user.username, 'email': user.email}, 200
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
            userToken = generateToken({'id':user.id, 'username':user.username, 'email':user.email})
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
        db.session.delete(user)
        db.session.commit()
        return {'status':200, 'message':'User deleted successfully'}, 200
    except Exception as e:
        print(e)
        return {'status':500, 'message':"Could not delete user"}, 500