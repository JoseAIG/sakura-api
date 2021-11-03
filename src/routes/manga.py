from flask import Blueprint, request
from controllers.manga_controller import getUserMangas, createManga, updateManga, deleteManga, getManga


manga_bp = Blueprint('manga_bp', __name__)


@manga_bp.route("/manga", methods=['GET', 'POST', 'PUT', 'DELETE'])
def manga():
    if(request.method == 'GET'):
        return getUserMangas()
    if(request.method == 'POST'):
        return createManga()
    if(request.method == 'PUT'):
        return updateManga()
    if(request.method == 'DELETE'):
        return deleteManga()

@manga_bp.route("/manga/<id>", methods=['GET'])
def manga_id(id):
    if(request.method == 'GET'):
        return getManga(id)
