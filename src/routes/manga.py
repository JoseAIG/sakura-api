from flask import Blueprint, request
from controllers.manga_controller import getAllMangas, getUserMangas, createManga, updateManga, deleteManga, getManga, searchMangas


manga_bp = Blueprint('manga_bp', __name__)


@manga_bp.route("/manga", methods=['GET', 'POST', 'PUT'])
def manga():
    if(request.method == 'GET'):
        return getUserMangas()
    if(request.method == 'POST'):
        return createManga()
    if(request.method == 'PUT'):
        return updateManga()

@manga_bp.route("/manga/<id>", methods=['GET', 'DELETE'])
def manga_id(id):
    if(request.method == 'GET'):
        return getManga(id)
    if(request.method == 'DELETE'):
        return deleteManga(id)

@manga_bp.route("/mangas", methods =['GET'])
def allMangas():
    if(request.method == 'GET'):
        return getAllMangas()

@manga_bp.route("/mangas/<keyword>", methods =['GET'])
def mangasKeyword(keyword):
    if(request.method == 'GET'):
        return searchMangas(keyword)