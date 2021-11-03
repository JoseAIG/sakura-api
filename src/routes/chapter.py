from flask import Blueprint, request
from controllers.chapter_controller import getChapter, getMangaChapters, updateChapter, deleteChapter, createChapter

chapter_bp = Blueprint('chapter_bp', __name__)

@chapter_bp.route("/<mangaID>/chapters", methods=['GET', 'POST', 'PUT', 'DELETE'])
def chapter(mangaID):
    if(request.method == 'GET'):
        return getMangaChapters(mangaID)
    if(request.method == 'POST'):
        return createChapter()
    if(request.method == 'PUT'):
        return updateChapter()
    if(request.method == 'DELETE'):
        return deleteChapter()

@chapter_bp.route("/<mangaID>/chapters/<id>", methods=['GET'])
def chapter_id(id,mangaID):
    if(request.method == 'GET'):
        return getChapter(id)