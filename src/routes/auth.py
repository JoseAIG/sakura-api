from flask import Blueprint, request
from controllers.auth_controller import registerUser, loginUser

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route("/register", methods=['POST'])
def register():
    if(request.method == 'POST'):
        return registerUser(request)


@auth_bp.route('/login', methods=['POST'])
def login():
    if(request.method == 'POST'):
        return loginUser(request)