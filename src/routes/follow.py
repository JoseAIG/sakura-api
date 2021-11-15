from flask import Blueprint, request
from controllers.following_controller import getFollowedMangas, followManga, unfollowManga

follow_bp = Blueprint('follow_bp', __name__)

@follow_bp.route("/follow/<mangaID>", methods=['POST'])
def follow(mangaID):
    if(request.method == 'POST'):
        return followManga(mangaID)

@follow_bp.route("/unfollow/<mangaID>", methods=['POST'])
def unfollow(mangaID):
    if(request.method == 'POST'):
        return unfollowManga(mangaID)

@follow_bp.route("/followed", methods=['GET'])
def getFollowed():
    if(request.method == 'GET'):
        return getFollowedMangas()