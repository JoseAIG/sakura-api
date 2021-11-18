from flask import Blueprint, request
from controllers.user_controller import getUser, updateUser, deleteUser, storeNotificationToken

user_bp = Blueprint('user_bp', __name__)


@user_bp.route("/user", methods=['GET', 'PUT', 'DELETE'])
def user():
    if(request.method == 'GET'):
        return getUser()
    if(request.method == 'PUT'):
        return updateUser()
    if(request.method == 'DELETE'):
        return deleteUser()

@user_bp.route("/user/notifications", methods=['POST'])
def userNotifications():
    if(request.method == 'POST'):
        return storeNotificationToken()