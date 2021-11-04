from flask import Blueprint, request
from controllers.chapter_controller import getChapter, getMangaChapters, updateChapter, deleteChapter, createChapter

chapter_bp = Blueprint('chapter_bp', __name__)

@chapter_bp.route("/manga/<mangaID>/chapters", methods=['GET', 'POST', 'PUT'])
def chapter(mangaID):
    if(request.method == 'GET'):
        return getMangaChapters(mangaID)
    if(request.method == 'POST'):
        return createChapter(mangaID)
    if(request.method == 'PUT'):
        return updateChapter()

@chapter_bp.route("/manga/<mangaID>/chapter/<number>", methods=['GET', 'DELETE'])
def chapter_id(mangaID, number):
    if(request.method == 'GET'):
        return getChapter(mangaID, number)
    if(request.method == 'DELETE'):
        return deleteChapter(mangaID, number)