import bcrypt
from database import db
from models.user import User
from helpers.jwt_tools import generateToken


def registerUser(request):
    try:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashedPassword = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode()

        print(username, email, password, hashedPassword)

        newUser = User(username, email, hashedPassword)
        db.session.add(newUser)
        db.session.commit()

        return {'status': 200, 'message': 'User created successfully.'}, 200
    except Exception as e:
        if('username' in e.args[0]):
            return {'status': 409, 'message': 'Username already registered'}, 409
        elif('email' in e.args[0]):
            return {'status': 409, 'message': 'e-mail already registered'}, 409
        else:
            return {'status': 500, 'message': 'Could not process register'}, 500
            

def loginUser(request):
    try:
        user = User.query.filter((User.username == request.form['user']) | (User.email == request.form['user'])).first()
        
        if(user is not None):
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), user.password.encode('utf-8')):
                userToken = generateToken({'id':user.id, 'username':user.username, 'email':user.email, 'admin':user.admin})
                print(userToken)
                return {'status': 200, 'message': 'Login successful', 'token': userToken}, 200
            else:
                return {'status': 401, 'message': 'Invalid credentials'}, 401
        else:
            return {'status': 401, 'message': 'User not registered'}, 401

    except Exception as e:
        print(e)
        return {'status': 500, 'message': 'Could not process login'}, 500