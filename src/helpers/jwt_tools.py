from flask import current_app, request
from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from functools import wraps


def expireDate(days: int):
    now = datetime.now()
    return now + timedelta(days)


def generateToken(data: dict):
    token = encode(payload={**data, "exp": expireDate(2)},key=current_app.config['SECRET_KEY'], algorithm="HS256")
    return token


def decodeToken(token: str):
    try:
        return decode(token, key=current_app.config['SECRET_KEY'], algorithms=["HS256"])
    except exceptions.InvalidTokenError:
        return {'status':401, 'message':'Invalid token'}, 401
    except exceptions.DecodeError:
        return {'status':401, 'message':'Invalid token'}, 401
    except exceptions.ExpiredSignatureError:
        return {'status':401, 'message':'Token expired'}, 401


# AUTH TOKEN REQUIRED DECORATOR
def authTokenRequired(f):
    @wraps(f)
    def function(*args, **kwargs):

        if('Authorization' in request.headers):
            token = request.headers['Authorization'].split(" ")[1]
            try:
                decode(token, key=current_app.config['SECRET_KEY'], algorithms=["HS256"])
            except exceptions.InvalidTokenError:
                return {'status':401, 'message':'Invalid token'}, 401
            except exceptions.DecodeError:
                return {'status':401, 'message':'Invalid token'}, 401
            except exceptions.ExpiredSignatureError:
                return {'status':401, 'message':'Token expired'}, 401
        else:
            return {'status':403, 'message':'No authorization header provided'}, 403

        return f(*args, **kwargs)

    return function